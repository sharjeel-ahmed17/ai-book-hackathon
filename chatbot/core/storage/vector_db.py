from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from chatbot.config.settings import settings
from chatbot.core.models.book_content import BookContent


logger = logging.getLogger(__name__)


class VectorDB:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        self.collection_name = "book_content"
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # Assuming OpenAI embeddings
            )
            logger.info(f"Created collection {self.collection_name}")

    def store_content(self, content: BookContent, embedding: List[float]) -> bool:
        """Store book content with its embedding in Qdrant"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=str(content.content_id),
                        vector=embedding,
                        payload={
                            "content_id": str(content.content_id),
                            "book_id": content.book_id,
                            "title": content.title,
                            "content_text": content.content_text,
                            "source_reference": content.source_reference,
                            "metadata": content.metadata.dict()
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            logger.error(f"Error storing content in Qdrant: {e}")
            return False

    def search_content(self, query_embedding: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant content based on query embedding"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            # Format results to match our content model
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content_id": result.payload.get("content_id"),
                    "book_id": result.payload.get("book_id"),
                    "title": result.payload.get("title"),
                    "content_text": result.payload.get("content_text"),
                    "source_reference": result.payload.get("source_reference"),
                    "metadata": result.payload.get("metadata"),
                    "relevance_score": result.score
                })

            return formatted_results
        except Exception as e:
            logger.error(f"Error searching content in Qdrant: {e}")
            return []

    def delete_content(self, content_id: str) -> bool:
        """Delete content from Qdrant by content_id"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[content_id]
                )
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting content from Qdrant: {e}")
            return False

    def get_all_content_ids(self) -> List[str]:
        """Get all content IDs in the collection"""
        try:
            records, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust as needed
                with_payload=False,
                with_vectors=False
            )
            return [str(record.id) for record in records]
        except Exception as e:
            logger.error(f"Error getting content IDs from Qdrant: {e}")
            return []