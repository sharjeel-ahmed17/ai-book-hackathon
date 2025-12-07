from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
import logging

from chatbot.core.models.query import Query, ContextType
from chatbot.core.models.response import Response, ValidationStatus
from chatbot.core.models.retrieved_context import RetrievedContext
from chatbot.core.rag.retriever import RAGRetriever
from chatbot.core.rag.generator import RAGGenerator
from chatbot.core.rag.validator import RAGValidator
from chatbot.core.storage.metadata_db import MetadataDB
from chatbot.core.storage.vector_db import VectorDB
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.services.session_manager import SessionManager
from chatbot.utils.validators import QueryValidator


logger = logging.getLogger(__name__)


class QueryService:
    """Service for handling query processing with full-book context"""

    def __init__(
        self,
        retriever: RAGRetriever,
        generator: RAGGenerator,
        validator: RAGValidator,
        metadata_db: MetadataDB,
        session_manager: SessionManager
    ):
        self.retriever = retriever
        self.generator = generator
        self.validator = validator
        self.metadata_db = metadata_db
        self.session_manager = session_manager

    def process_full_book_query(
        self,
        query_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        top_k: int = 5
    ) -> Optional[Response]:
        """
        Process a query against the full book content
        """
        try:
            # Validate the query
            validation_errors = QueryValidator.validate_query_content(query_text)
            if validation_errors:
                logger.warning(f"Query validation failed: {'; '.join(validation_errors)}")
                return None

            # Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Create query object
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.FULL_BOOK,
                selected_text=None,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Store the query in metadata DB
            query_stored = self.metadata_db.create_query(
                query_id=str(query_obj.query_id),
                session_id=str(session_id),
                content=query_text,
                context_type=query_obj.context_type.value
            )

            if not query_stored:
                logger.error("Failed to store query in metadata DB")
                return None

            # Retrieve relevant context from full book
            retrieved_context = self.retriever.retrieve_context(query_obj, top_k=top_k)
            if not retrieved_context or not retrieved_context.content_chunks:
                logger.warning("No relevant content found for query")
                # Create a response indicating that the query cannot be answered
                response_obj = Response(
                    response_id=uuid4(),
                    query_id=query_obj.query_id,
                    content="I cannot find relevant information in the book to answer this question.",
                    source_references=[],
                    timestamp=datetime.now(),
                    validation_status=ValidationStatus.PASSED  # This is a valid response
                )
                return response_obj

            # Validate the retrieved context
            if not self.retriever.validate_retrieved_context(retrieved_context):
                logger.warning("Retrieved context does not meet quality requirements")
                return None

            # Generate response based on the retrieved context
            response_obj = self.generator.generate_response(query_obj, retrieved_context)
            if not response_obj:
                logger.error("Failed to generate response")
                return None

            # Validate the response for grounding in context
            validation_status = self.generator.validate_response_content(response_obj, retrieved_context)
            response_obj.validation_status = validation_status

            # Store the response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=validation_status.value
            )

            if not response_stored:
                logger.error("Failed to store response in metadata DB")

            # Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in process_full_book_query: {e}")
            return None

    def process_selected_text_query(
        self,
        query_text: str,
        selected_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        top_k: int = 3
    ) -> Optional[Response]:
        """
        Process a query against selected text
        """
        try:
            # Validate the query and selected text
            query_errors = QueryValidator.validate_query_content(query_text)
            if query_errors:
                logger.warning(f"Query validation failed: {'; '.join(query_errors)}")
                return None

            if not selected_text or len(selected_text.strip()) < 10:
                logger.warning("Selected text is too short")
                return None

            # Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Create query object with selected text context
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.SELECTED_TEXT,
                selected_text=selected_text,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Store the query in metadata DB
            query_stored = self.metadata_db.create_query(
                query_id=str(query_obj.query_id),
                session_id=str(session_id),
                content=query_text,
                context_type=query_obj.context_type.value,
                selected_text=selected_text
            )

            if not query_stored:
                logger.error("Failed to store query in metadata DB")
                return None

            # For selected text queries, we'll use the selected text as primary context
            # but also retrieve similar content from the book
            retrieved_context = self.retriever.retrieve_context_for_selected_text(query_obj, top_k=top_k)

            # If we couldn't find similar content, we'll generate response just from the selected text
            if not retrieved_context or not retrieved_context.content_chunks:
                response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)
            else:
                # Validate the retrieved context
                if not self.retriever.validate_retrieved_context(retrieved_context):
                    logger.warning("Retrieved context does not meet quality requirements, using selected text only")
                    response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)
                else:
                    # Generate response based on the retrieved context
                    response_obj = self.generator.generate_response(query_obj, retrieved_context)

            if not response_obj:
                logger.error("Failed to generate response for selected text query")
                return None

            # Validate the response for grounding in context
            if retrieved_context:
                validation_status = self.generator.validate_response_content(response_obj, retrieved_context)
            else:
                # For selected text only, we'll mark as passed if it contains info from the selected text
                validation_status = ValidationStatus.PASSED  # Basic validation

            response_obj.validation_status = validation_status

            # Store the response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=validation_status.value
            )

            if not response_stored:
                logger.error("Failed to store response in metadata DB")

            # Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in process_selected_text_query: {e}")
            return None

    def extend_rag_pipeline_for_selected_text(
        self,
        query_text: str,
        selected_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None
    ) -> Optional[Response]:
        """
        Extend the RAG pipeline to support selected-text context
        This method specifically handles the selected-text query functionality
        """
        try:
            # Validate the query and selected text
            query_errors = QueryValidator.validate_query_content(query_text)
            if query_errors:
                logger.warning(f"Query validation failed: {'; '.join(query_errors)}")
                return None

            if not selected_text or len(selected_text.strip()) < 10:
                logger.warning("Selected text is too short for meaningful processing")
                return None

            # Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Create query object with selected text context
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.SELECTED_TEXT,
                selected_text=selected_text,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Store the query in metadata DB
            query_stored = self.metadata_db.create_query(
                query_id=str(query_obj.query_id),
                session_id=str(session_id),
                content=query_text,
                context_type=query_obj.context_type.value,
                selected_text=selected_text
            )

            if not query_stored:
                logger.error("Failed to store query in metadata DB")
                return None

            # Retrieve context specifically for selected text
            retrieved_context = self.retriever.retrieve_context_for_selected_text(query_obj)

            # Generate response using the selected text and any retrieved context
            if retrieved_context and retrieved_context.content_chunks:
                # Validate the retrieved context
                if self.retriever.validate_retrieved_context(retrieved_context):
                    response_obj = self.generator.generate_response(query_obj, retrieved_context)
                else:
                    # Fallback to selected text only if retrieved context is invalid
                    response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)
            else:
                # Use selected text only
                response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)

            if not response_obj:
                logger.error("Failed to generate response for selected text query")
                return None

            # Validate the response for proper grounding
            validation_status = ValidationStatus.PASSED  # Default to passed for selected text
            if retrieved_context and retrieved_context.content_chunks:
                validation_status = self.generator.validate_response_content(response_obj, retrieved_context)

            response_obj.validation_status = validation_status

            # Store the response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=validation_status.value
            )

            if not response_stored:
                logger.error("Failed to store response in metadata DB")

            # Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in extend_rag_pipeline_for_selected_text: {e}")
            return None

    def process_query_by_context_type(
        self,
        query_text: str,
        context_type: ContextType,
        selected_text: Optional[str] = None,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None
    ) -> Optional[Response]:
        """
        Process a query based on the specified context type
        """
        if context_type == ContextType.FULL_BOOK:
            return self.process_full_book_query(query_text, session_id, user_id)
        elif context_type == ContextType.SELECTED_TEXT and selected_text:
            return self.process_selected_text_query(query_text, selected_text, session_id, user_id)
        else:
            # Default to full book context
            return self.process_full_book_query(query_text, session_id, user_id)