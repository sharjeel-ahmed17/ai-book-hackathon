from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ContentChunk(BaseModel):
    text: str
    source_reference: str
    relevance_score: Optional[float] = None


class RetrievalMetadata(BaseModel):
    retrieval_method: str
    confidence_score: Optional[float] = None
    timestamp: datetime = datetime.now()


class RetrievedContext(BaseModel):
    context_id: UUID
    query_id: UUID
    content_chunks: List[ContentChunk]
    metadata: RetrievalMetadata