from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


class ContextType(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    SELECTED_TEXT = "SELECTED_TEXT"


class SourceReference(BaseModel):
    reference: str
    text: str
    relevance_score: Optional[float] = None


class Query(BaseModel):
    query_id: UUID
    session_id: UUID
    content: str
    context_type: ContextType
    selected_text: Optional[str] = None
    timestamp: datetime
    source_references: List[SourceReference] = []

    class Config:
        use_enum_values = True


class QueryCreateRequest(BaseModel):
    query: str
    context_type: ContextType = ContextType.FULL_BOOK
    selected_text: Optional[str] = None
    session_id: Optional[UUID] = None