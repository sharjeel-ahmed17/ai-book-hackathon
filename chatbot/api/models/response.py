from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from chatbot.core.models.response import ValidationStatus


class SourceReferenceResponse(BaseModel):
    reference: str = Field(..., description="Reference to where in the book this information originated")
    text: str = Field(..., description="Original text from the book that supports this answer")
    relevance_score: Optional[float] = Field(None, description="How relevant this chunk is to the query")
    page_number: Optional[int] = Field(None, description="Page number where the information originated")
    chapter: Optional[str] = Field(None, description="Chapter where the information originated")
    section: Optional[str] = Field(None, description="Section where the information originated")
    content_id: Optional[str] = Field(None, description="ID of the content chunk")


class QueryResponse(BaseModel):
    response_id: UUID = Field(..., description="Unique identifier for this response")
    answer: str = Field(..., description="The chatbot's answer to the query")
    source_references: List[SourceReferenceResponse] = Field(default_factory=list, description="List of source references used")
    session_id: UUID = Field(..., description="Session identifier")
    validation_status: ValidationStatus = Field(..., description="Status of hallucination check")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall health status")
    timestamp: str = Field(..., description="Timestamp of the health check")
    service: str = Field(..., description="Name of the service")
    version: str = Field(..., description="Version of the service")
    dependencies: dict = Field(..., description="Status of dependencies")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")


class IngestionSuccessResponse(BaseModel):
    status: str = Field(..., description="Status of the ingestion operation")
    content_id: str = Field(..., description="UUID of the ingested content")
    chunks_processed: int = Field(..., description="Number of content chunks processed")
    processing_time_ms: int = Field(..., description="Time taken to process in milliseconds")