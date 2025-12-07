from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class QueryContextDefault(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    SELECTED_TEXT = "SELECTED_TEXT"


class ResponseFormat(str, Enum):
    DETAILED = "DETAILED"
    CONCISE = "CONCISE"
    BULLETED = "BULLETED"


class UserSessionPreference(BaseModel):
    preference_id: UUID
    session_id: UUID
    query_context_default: QueryContextDefault = QueryContextDefault.FULL_BOOK
    response_format: ResponseFormat = ResponseFormat.DETAILED
    source_citation_preference: bool = True
    created_at: datetime
    updated_at: datetime