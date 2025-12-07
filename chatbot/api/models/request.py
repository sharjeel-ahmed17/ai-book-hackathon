from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from chatbot.core.models.query import ContextType


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The user's question or query")
    context_type: ContextType = Field(default=ContextType.FULL_BOOK, description="Type of context to search (FULL_BOOK or SELECTED_TEXT)")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Specific text provided by user for selected-text queries")
    session_id: Optional[UUID] = Field(None, description="Session identifier for conversation history")


class IngestionRequest(BaseModel):
    book_id: str = Field(..., min_length=1, description="Unique identifier for the book")
    title: str = Field(..., min_length=1, description="Title of the book")
    content: str = Field(..., min_length=1, description="Full book content in markdown format")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata about the book")


class IngestionResponse(BaseModel):
    status: str = Field(..., description="Status of the ingestion operation")
    content_id: Optional[str] = Field(None, description="UUID of the ingested content")
    chunks_processed: int = Field(..., description="Number of content chunks processed")
    processing_time_ms: int = Field(..., description="Time taken to process in milliseconds")