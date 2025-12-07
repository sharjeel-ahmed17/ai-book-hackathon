from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


class ValidationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    PENDING = "PENDING"


class SourceReference(BaseModel):
    reference: str
    text: str
    relevance_score: Optional[float] = None
    page_number: Optional[int] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    content_id: Optional[str] = None


class Response(BaseModel):
    response_id: UUID
    query_id: UUID
    content: str
    source_references: List[SourceReference]
    timestamp: datetime
    validation_status: ValidationStatus