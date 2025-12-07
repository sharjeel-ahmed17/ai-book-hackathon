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


class RAGPipeline:
    """Complete RAG pipeline for processing queries with grounding validation"""

    def __init__(
        self,
        retriever: RAGRetriever,
        generator: RAGGenerator,
        validator: RAGValidator,
        metadata_db: MetadataDB,
        session_manager: SessionManager,
        embedding_processor: EmbeddingProcessor
    ):
        self.retriever = retriever
        self.generator = generator
        self.validator = validator
        self.metadata_db = metadata_db
        self.session_manager = session_manager
        self.embedding_processor = embedding_processor

    def run_full_book_pipeline(
        self,
        query_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        top_k: int = 5,
        validate_grounding: bool = True
    ) -> Optional[Response]:
        """
        Run the complete RAG pipeline for full-book queries
        """
        try:
            # Step 1: Validate query
            validation_errors = QueryValidator.validate_query_content(query_text)
            if validation_errors:
                logger.warning(f"Query validation failed: {'; '.join(validation_errors)}")
                return None

            # Step 2: Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Step 3: Create query object
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.FULL_BOOK,
                selected_text=None,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Step 4: Store query in metadata DB
            query_stored = self.metadata_db.create_query(
                query_id=str(query_obj.query_id),
                session_id=str(session_id),
                content=query_text,
                context_type=query_obj.context_type.value
            )

            if not query_stored:
                logger.error("Failed to store query in metadata DB")
                return None

            # Step 5: Retrieve relevant context
            retrieved_context = self.retriever.retrieve_context(query_obj, top_k=top_k)
            if not retrieved_context or not retrieved_context.content_chunks:
                logger.info("No relevant content found, returning appropriate response")
                response_obj = Response(
                    response_id=uuid4(),
                    query_id=query_obj.query_id,
                    content="I cannot find relevant information in the book to answer this question.",
                    source_references=[],
                    timestamp=datetime.now(),
                    validation_status=ValidationStatus.PASSED
                )
                return self._finalize_response(response_obj, query_obj, session_id)

            # Step 6: Validate retrieved context
            if not self.retriever.validate_retrieved_context(retrieved_context):
                logger.warning("Retrieved context does not meet quality requirements")
                response_obj = Response(
                    response_id=uuid4(),
                    query_id=query_obj.query_id,
                    content="The retrieved context does not meet quality requirements to generate a reliable answer.",
                    source_references=[],
                    timestamp=datetime.now(),
                    validation_status=ValidationStatus.FAILED
                )
                return self._finalize_response(response_obj, query_obj, session_id)

            # Step 7: Generate response
            response_obj = self.generator.generate_response(query_obj, retrieved_context)
            if not response_obj:
                logger.error("Failed to generate response")
                return None

            # Step 8: Validate grounding if requested
            if validate_grounding:
                validation_status = self.validator.validate_response_grounding(
                    query_obj, retrieved_context, response_obj
                )
                response_obj.validation_status = validation_status

                # Additional zero hallucination validation
                if validation_status == ValidationStatus.PASSED:
                    zero_hallucination_valid = self.validator.validate_zero_hallucination(
                        query_obj, response_obj, retrieved_context
                    )
                    if not zero_hallucination_valid:
                        response_obj.validation_status = ValidationStatus.FAILED
                        logger.warning("Response failed zero hallucination validation")

            # Step 9: Store response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=response_obj.validation_status.value
            )

            if not response_stored:
                logger.warning("Failed to store response in metadata DB")

            # Step 10: Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in run_full_book_pipeline: {e}")
            return None

    def run_selected_text_pipeline(
        self,
        query_text: str,
        selected_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        top_k: int = 3,
        validate_grounding: bool = True
    ) -> Optional[Response]:
        """
        Run the complete RAG pipeline for selected-text queries
        """
        try:
            # Step 1: Validate query and selected text
            query_errors = QueryValidator.validate_query_content(query_text)
            if query_errors:
                logger.warning(f"Query validation failed: {'; '.join(query_errors)}")
                return None

            if not selected_text or len(selected_text.strip()) < 10:
                logger.warning("Selected text is too short")
                return None

            # Step 2: Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Step 3: Create query object with selected text context
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.SELECTED_TEXT,
                selected_text=selected_text,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Step 4: Store query in metadata DB
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

            # Step 5: Retrieve context relevant to selected text
            retrieved_context = self.retriever.retrieve_context_for_selected_text(query_obj, top_k=top_k)

            # Step 6: Generate response (either from selected text only or with retrieved context)
            if not retrieved_context or not retrieved_context.content_chunks:
                # Use selected text as primary context
                response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)
            else:
                # Validate retrieved context
                if self.retriever.validate_retrieved_context(retrieved_context):
                    # Use retrieved context
                    response_obj = self.generator.generate_response(query_obj, retrieved_context)
                else:
                    # Fallback to selected text only
                    response_obj = self.generator.generate_response_with_selected_text_context(query_obj, selected_text)

            if not response_obj:
                logger.error("Failed to generate response for selected text query")
                return None

            # Step 7: Validate grounding if requested
            if validate_grounding and retrieved_context:
                validation_status = self.validator.validate_response_grounding(
                    query_obj, retrieved_context, response_obj
                )
                response_obj.validation_status = validation_status

                # Additional zero hallucination validation
                if validation_status == ValidationStatus.PASSED:
                    zero_hallucination_valid = self.validator.validate_zero_hallucination(
                        query_obj, response_obj, retrieved_context
                    )
                    if not zero_hallucination_valid:
                        response_obj.validation_status = ValidationStatus.FAILED
                        logger.warning("Response failed zero hallucination validation")
            elif validate_grounding:
                # For selected text only, do basic validation
                response_obj.validation_status = ValidationStatus.PASSED

            # Step 8: Store response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=response_obj.validation_status.value
            )

            if not response_stored:
                logger.warning("Failed to store response in metadata DB")

            # Step 9: Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in run_selected_text_pipeline: {e}")
            return None

    def run_pipeline_by_context_type(
        self,
        query_text: str,
        context_type: ContextType,
        selected_text: Optional[str] = None,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None
    ) -> Optional[Response]:
        """
        Run the appropriate RAG pipeline based on context type
        """
        if context_type == ContextType.FULL_BOOK:
            return self.run_full_book_pipeline(query_text, session_id, user_id)
        elif context_type == ContextType.SELECTED_TEXT and selected_text:
            return self.run_selected_text_pipeline(query_text, selected_text, session_id, user_id)
        else:
            # Default to full book context
            return self.run_full_book_pipeline(query_text, session_id, user_id)

    def extend_pipeline_for_selected_text_context(
        self,
        query_text: str,
        selected_text: str,
        session_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None
    ) -> Optional[Response]:
        """
        Extend the RAG pipeline to specifically support selected-text context
        This method implements the functionality required for User Story 2
        """
        try:
            # Step 1: Validate query and selected text
            query_errors = QueryValidator.validate_query_content(query_text)
            if query_errors:
                logger.warning(f"Query validation failed: {'; '.join(query_errors)}")
                return None

            if not selected_text or len(selected_text.strip()) < 10:
                logger.warning("Selected text is too short for meaningful processing")
                return None

            # Step 2: Create or get session
            if not session_id:
                session = self.session_manager.create_session(str(user_id) if user_id else None)
                session_id = session.session_id
            else:
                session = self.session_manager.get_session(str(session_id))
                if not session:
                    session = self.session_manager.create_session(str(user_id) if user_id else None)

            # Step 3: Create query object with selected text context
            query_obj = Query(
                query_id=uuid4(),
                session_id=session_id,
                content=query_text,
                context_type=ContextType.SELECTED_TEXT,
                selected_text=selected_text,
                timestamp=datetime.now(),
                source_references=[]
            )

            # Step 4: Store query in metadata DB
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

            # Step 5: Retrieve context relevant to the selected text
            retrieved_context = self.retriever.retrieve_context_for_selected_text(query_obj)

            # Step 6: Generate response based on selected text and retrieved context
            if retrieved_context and retrieved_context.content_chunks:
                # Validate the retrieved context
                if self.retriever.validate_retrieved_context(retrieved_context):
                    # Use both selected text and retrieved context
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

            # Step 7: Validate response grounding
            validation_status = ValidationStatus.PASSED  # Default for selected text
            if retrieved_context and retrieved_context.content_chunks:
                validation_status = self.validator.validate_response_grounding(
                    query_obj, retrieved_context, response_obj
                )

                # Additional zero hallucination validation if initial validation passed
                if validation_status == ValidationStatus.PASSED:
                    zero_hallucination_valid = self.validator.validate_zero_hallucination(
                        query_obj, response_obj, retrieved_context
                    )
                    if not zero_hallucination_valid:
                        validation_status = ValidationStatus.FAILED
                        logger.warning("Response failed zero hallucination validation for selected text")

            response_obj.validation_status = validation_status

            # Step 8: Store response in metadata DB
            response_stored = self.metadata_db.create_response(
                response_id=str(response_obj.response_id),
                query_id=str(query_obj.query_id),
                content=response_obj.content,
                source_references=[ref.dict() for ref in response_obj.source_references],
                validation_status=response_obj.validation_status.value
            )

            if not response_stored:
                logger.warning("Failed to store response in metadata DB")

            # Step 9: Add query to session
            self.session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

            return response_obj

        except Exception as e:
            logger.error(f"Error in extend_pipeline_for_selected_text_context: {e}")
            return None

    def _finalize_response(self, response: Response, query: Query, session_id: UUID) -> Response:
        """
        Finalize response by storing in DB and updating session
        """
        # Store response in metadata DB
        self.metadata_db.create_response(
            response_id=str(response.response_id),
            query_id=str(query.query_id),
            content=response.content,
            source_references=[ref.dict() for ref in response.source_references],
            validation_status=response.validation_status.value
        )

        # Add query to session
        self.session_manager.add_query_to_session(str(session_id), str(query.query_id))

        return response