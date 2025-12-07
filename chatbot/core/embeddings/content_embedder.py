from typing import List, Optional
from uuid import UUID
import logging
from chatbot.core.models.book_content import BookContent
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.core.storage.vector_db import VectorDB


logger = logging.getLogger(__name__)


class ContentEmbedder:
    """Handles embedding generation and storage for book content"""

    def __init__(self, embedding_processor: EmbeddingProcessor, vector_db: VectorDB):
        self.embedding_processor = embedding_processor
        self.vector_db = vector_db

    def embed_and_store_single_content(self, book_content: BookContent) -> bool:
        """
        Generate embedding for a single piece of book content and store it in vector DB
        """
        try:
            # Generate embedding for the content
            embedding = self.embedding_processor.generate_embedding(book_content.content_text)

            if not embedding:
                logger.error(f"Failed to generate embedding for content: {book_content.content_id}")
                return False

            # Store in vector database
            success = self.vector_db.store_content(book_content, embedding)

            if success:
                logger.info(f"Successfully embedded and stored content: {book_content.content_id}")
                return True
            else:
                logger.error(f"Failed to store content in vector DB: {book_content.content_id}")
                return False

        except Exception as e:
            logger.error(f"Error in embed_and_store_single_content: {e}")
            return False

    def embed_and_store_batch(self, book_contents: List[BookContent]) -> int:
        """
        Generate embeddings for a batch of book content and store them in vector DB
        Returns the number of successfully processed contents
        """
        success_count = 0

        try:
            # Extract text from all contents
            texts = [content.content_text for content in book_contents]

            # Generate embeddings in batch if the embedding processor supports it
            embeddings = self.embedding_processor.generate_embeddings_batch(texts)

            if not embeddings or len(embeddings) != len(book_contents):
                logger.warning("Batch embedding failed, falling back to individual processing")
                # Fall back to individual processing
                for content in book_contents:
                    if self.embed_and_store_single_content(content):
                        success_count += 1
                return success_count

            # Store all contents with their embeddings
            for content, embedding in zip(book_contents, embeddings):
                success = self.vector_db.store_content(content, embedding)
                if success:
                    success_count += 1
                else:
                    logger.error(f"Failed to store content in vector DB: {content.content_id}")

            return success_count

        except Exception as e:
            logger.error(f"Error in embed_and_store_batch: {e}")
            # Fall back to individual processing
            for content in book_contents:
                if self.embed_and_store_single_content(content):
                    success_count += 1
            return success_count

    def embed_text_for_query(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for query text
        """
        try:
            return self.embedding_processor.generate_embedding(text)
        except Exception as e:
            logger.error(f"Error generating embedding for query: {e}")
            return None

    def update_content_embedding(self, content_id: str, new_content: str) -> bool:
        """
        Update the embedding for existing content
        """
        try:
            # First, delete the old content from vector DB
            self.vector_db.delete_content(content_id)

            # This method would need to retrieve the full BookContent object to update it
            # For now, we'll just return False as this requires more complex implementation
            logger.warning("Update content embedding requires full BookContent object, not just content text")
            return False

        except Exception as e:
            logger.error(f"Error updating content embedding: {e}")
            return False