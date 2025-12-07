from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging
from datetime import datetime

from chatbot.api.models.request import IngestionRequest
from chatbot.api.models.response import IngestionSuccessResponse
from chatbot.core.models.book_content import BookContent
from chatbot.core.embeddings.content_embedder import ContentEmbedder
from chatbot.services.content_converter import ContentConverter
from chatbot.services.chunker import TextChunker
from chatbot.config.settings import settings


logger = logging.getLogger(__name__)
router = APIRouter()


# In a real implementation, these would be dependency-injected
# For now, we'll import and instantiate them directly
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.core.storage.vector_db import VectorDB

embedding_processor = EmbeddingProcessor()
vector_db = VectorDB()
content_embedder = ContentEmbedder(embedding_processor, vector_db)


@router.post("/ingest", summary="Ingest book content for retrieval", response_model=IngestionSuccessResponse)
async def ingest_content(request: IngestionRequest):
    """
    Ingest book content for retrieval by the RAG system.
    """
    start_time = datetime.now()

    try:
        # Validate the request
        if not request.book_id or not request.title or not request.content:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="book_id, title, and content are required fields"
            )

        # Convert content based on format
        # For now, we'll assume it's markdown format and use the converter
        converter = ContentConverter()
        book_contents = converter.convert_from_markdown(
            content=request.content,
            book_id=request.book_id,
            title=request.title,
            source_reference=f"book:{request.book_id}"
        )

        # If conversion didn't work well, try text conversion as fallback
        if not book_contents or len(book_contents) == 0:
            book_contents = converter.convert_from_text(
                content=request.content,
                book_id=request.book_id,
                title=request.title,
                source_reference=f"book:{request.book_id}"
            )

        # Chunk the content if it's too large
        chunked_contents = []
        for content in book_contents:
            if len(content.content_text) > settings.max_query_length * 2:  # If content is too large
                chunked = TextChunker.chunk_book_content(
                    content,
                    max_chunk_size=1000,
                    overlap=100
                )
                chunked_contents.extend(chunked)
            else:
                chunked_contents.append(content)

        # Embed and store the content
        success_count = content_embedder.embed_and_store_batch(chunked_contents)

        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        if success_count > 0:
            return IngestionSuccessResponse(
                status="success",
                content_id=str(chunked_contents[0].content_id) if chunked_contents else "",
                chunks_processed=success_count,
                processing_time_ms=processing_time
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to ingest any content chunks"
            )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in content ingestion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during content ingestion: {str(e)}"
        )


@router.post("/ingest/text", summary="Ingest plain text content", response_model=IngestionSuccessResponse)
async def ingest_text_content(book_id: str, title: str, content: str):
    """
    Ingest plain text content for retrieval by the RAG system.
    """
    start_time = datetime.now()

    try:
        # Validate the request
        if not book_id or not title or not content:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="book_id, title, and content are required fields"
            )

        # Convert content to BookContent format
        converter = ContentConverter()
        book_contents = converter.convert_from_text(
            content=content,
            book_id=book_id,
            title=title,
            source_reference=f"text:{book_id}"
        )

        # Embed and store the content
        success_count = content_embedder.embed_and_store_batch(book_contents)

        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        if success_count > 0:
            return IngestionSuccessResponse(
                status="success",
                content_id=str(book_contents[0].content_id) if book_contents else "",
                chunks_processed=success_count,
                processing_time_ms=processing_time
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to ingest any content"
            )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in text content ingestion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during text content ingestion: {str(e)}"
        )


@router.delete("/ingest/{content_id}", summary="Delete ingested content")
async def delete_content(content_id: str):
    """
    Delete previously ingested content by content_id.
    """
    try:
        success = vector_db.delete_content(content_id)

        if success:
            return {"status": "deleted", "content_id": content_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with ID {content_id} not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during content deletion: {str(e)}"
        )