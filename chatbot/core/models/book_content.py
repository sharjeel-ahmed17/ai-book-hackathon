from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime


class ContentMetadata(BaseModel):
    chapter_number: Optional[int] = None
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BookContent(BaseModel):
    content_id: UUID
    book_id: str
    title: str
    content_text: str
    metadata: ContentMetadata = ContentMetadata()
    embedding_vector: Optional[List[float]] = None
    source_reference: str