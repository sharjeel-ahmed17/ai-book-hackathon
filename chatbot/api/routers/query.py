from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
import logging

from chatbot.api.models.request import QueryRequest
from chatbot.api.models.response import QueryResponse, ErrorResponse
from chatbot.core.models.query import Query, QueryCreateRequest
from chatbot.core.rag.retriever import RAGRetriever
from chatbot.core.rag.generator import RAGGenerator
from chatbot.core.rag.validator import RAGValidator
from chatbot.core.storage.metadata_db import MetadataDB
from chatbot.core.storage.vector_db import VectorDB
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.services.session_manager import SessionManager
from chatbot.config.settings import settings
from chatbot.utils.validators import QueryValidator


logger = logging.getLogger(__name__)
router = APIRouter()


# We'll initialize the required services here
# In a real application, these would be dependency-injected
metadata_db = MetadataDB()
vector_db = VectorDB()
embedding_processor = EmbeddingProcessor()
retriever = RAGRetriever(vector_db, metadata_db, embedding_processor)
generator = RAGGenerator()
validator = RAGValidator(embedding_processor)
session_manager = SessionManager(metadata_db)


@router.post("/query", summary="Process a user query against the book content", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query against the book content.
    """
    try:
        # Validate the query
        validation_errors = QueryValidator.validate_query_content(request.query)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Query validation failed: {'; '.join(validation_errors)}"
            )

        # Create or get session
        session_id = request.session_id or uuid4()
        if str(session_id) not in session_manager.active_sessions:
            session_manager.create_session()

        # Create query object
        query_obj = Query(
            query_id=uuid4(),
            session_id=session_id,
            content=request.query,
            context_type=request.context_type,
            selected_text=request.selected_text,
            timestamp=datetime.now(),
            source_references=[]
        )

        # Store the query in metadata DB
        metadata_db.create_query(
            query_id=str(query_obj.query_id),
            session_id=str(session_id),
            content=request.query,
            context_type=request.context_type.value,
            selected_text=request.selected_text
        )

        # Retrieve relevant context
        retrieved_context = retriever.retrieve_context_by_type(query_obj)
        if not retrieved_context or not retrieved_context.content_chunks:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No relevant content found in the book to answer this query"
            )

        # Validate the retrieved context
        if not retriever.validate_retrieved_context(retrieved_context):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Retrieved context does not meet quality requirements"
            )

        # Generate response based on context
        response_obj = None
        if request.context_type.value == "SELECTED_TEXT" and request.selected_text:
            response_obj = generator.generate_response_with_selected_text_context(query_obj, request.selected_text)
        else:
            response_obj = generator.generate_response(query_obj, retrieved_context)

        if not response_obj:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate response"
            )

        # Validate the response for grounding in context
        validation_status = generator.validate_response_content(response_obj, retrieved_context)
        response_obj.validation_status = validation_status

        # Store the response in metadata DB
        metadata_db.create_response(
            response_id=str(response_obj.response_id),
            query_id=str(query_obj.query_id),
            content=response_obj.content,
            source_references=[ref.dict() for ref in response_obj.source_references],
            validation_status=validation_status.value
        )

        # Add query to session
        session_manager.add_query_to_session(str(session_id), str(query_obj.query_id))

        # Create API response
        api_response = QueryResponse(
            response_id=response_obj.response_id,
            answer=response_obj.content,
            source_references=[
                {
                    "reference": ref.reference,
                    "text": ref.text,
                    "relevance_score": ref.relevance_score,
                    "page_number": ref.page_number,
                    "chapter": ref.chapter,
                    "section": ref.section,
                    "content_id": ref.content_id
                } for ref in response_obj.source_references
            ],
            session_id=session_id,
            validation_status=response_obj.validation_status
        )

        return api_response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing query"
        )


@router.get("/session/{session_id}", summary="Get session details")
async def get_session(session_id: str):
    """
    Get details about a specific session.
    """
    try:
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        return {
            "session_id": str(session.session_id),
            "user_id": str(session.user_id) if session.user_id else None,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "query_count": len(session.queries)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving session"
        )