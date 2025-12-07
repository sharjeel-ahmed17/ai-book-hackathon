from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime


class QueryInSession(BaseModel):
    query_id: UUID
    timestamp: datetime


class SessionMetadata(BaseModel):
    tags: List[str] = []
    properties: Dict[str, Any] = {}


class ConversationSession(BaseModel):
    session_id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    last_activity: datetime
    queries: List[QueryInSession] = []
    metadata: SessionMetadata = SessionMetadata()