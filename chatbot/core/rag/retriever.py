from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import logging
from chatbot.core.storage.vector_db import VectorDB
from chatbot.core.storage.metadata_db import MetadataDB
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.core.models.retrieved_context import RetrievedContext, ContentChunk, RetrievalMetadata
from chatbot.core.models.query import Query, ContextType
from chatbot.utils.validators import QueryValidator


logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieves relevant context from book content based on user queries"""

    def __init__(self, vector_db: VectorDB, metadata_db: MetadataDB, embedding_processor: EmbeddingProcessor):
        self.vector_db = vector_db
        self.metadata_db = metadata_db
        self.embedding_processor = embedding_processor

    def retrieve_context(self, query: Query, top_k: int = 5) -> Optional[RetrievedContext]:
        """
        Retrieve relevant context for a query
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_processor.generate_embedding(query.content)
            if not query_embedding:
                logger.error("Failed to generate embedding for query")
                return None

            # Search for relevant content in vector database
            search_results = self.vector_db.search_content(query_embedding, limit=top_k)

            # Convert search results to content chunks with enhanced source information
            content_chunks = []
            for result in search_results:
                # Extract additional source information from the result
                source_reference = result["source_reference"]
                content_text = result["content_text"]
                relevance_score = result["relevance_score"]

                # Try to extract additional metadata from the result
                metadata = result.get("metadata", {})

                # Create content chunk with enhanced source information
                content_chunk = ContentChunk(
                    text=content_text,
                    source_reference=source_reference,
                    relevance_score=relevance_score
                )

                # Enhance the content chunk with additional source information
                # For now, we'll add it to the source reference field
                if metadata and isinstance(metadata, dict):
                    if "page_number" in metadata:
                        content_chunk.source_reference += f" (Page: {metadata['page_number']})"
                    if "chapter" in metadata:
                        content_chunk.source_reference += f" (Chapter: {metadata['chapter']})"
                    if "section_title" in metadata:
                        content_chunk.source_reference += f" (Section: {metadata['section_title']})"

                content_chunks.append(content_chunk)

            # Create retrieval metadata
            retrieval_metadata = RetrievalMetadata(
                retrieval_method="vector_similarity",
                confidence_score=search_results[0]["relevance_score"] if search_results else 0.0,
                timestamp=datetime.now()
            )

            # Create retrieved context object
            retrieved_context = RetrievedContext(
                context_id=UUID(str(query.query_id)),  # Using query ID as context ID for now
                query_id=query.query_id,
                content_chunks=content_chunks,
                metadata=retrieval_metadata
            )

            return retrieved_context

        except Exception as e:
            logger.error(f"Error in retrieve_context: {e}")
            return None

    def retrieve_context_for_selected_text(self, query: Query, top_k: int = 5) -> Optional[RetrievedContext]:
        """
        Retrieve context specifically for selected text queries
        In this case, we use the selected text as the primary context
        """
        try:
            if not query.selected_text:
                logger.error("No selected text provided for selected-text query")
                return None

            # Generate embedding for the query
            query_embedding = self.embedding_processor.generate_embedding(query.content)
            if not query_embedding:
                logger.error("Failed to generate embedding for query")
                return None

            # For selected-text queries, we first look for content similar to the selected text
            selected_text_embedding = self.embedding_processor.generate_embedding(query.selected_text)
            if not selected_text_embedding:
                logger.error("Failed to generate embedding for selected text")
                return None

            # Search for content similar to the selected text
            search_results = self.vector_db.search_content(selected_text_embedding, limit=top_k)

            # Filter results to ensure they're relevant to the actual query as well
            filtered_results = []
            for result in search_results:
                # Calculate similarity between query and the retrieved content
                content_embedding = self.embedding_processor.generate_embedding(result["content_text"])
                if content_embedding:
                    query_similarity = self.embedding_processor.calculate_similarity(query_embedding, content_embedding)
                    # Only include if it's reasonably similar to the query
                    if query_similarity > 0.3:  # Threshold can be adjusted
                        result["query_similarity"] = query_similarity
                        filtered_results.append(result)

            # Convert filtered results to content chunks with enhanced source information
            content_chunks = []
            for result in filtered_results:
                # Extract additional source information from the result
                source_reference = result["source_reference"]
                content_text = result["content_text"]
                relevance_score = result["relevance_score"]

                # Try to extract additional metadata from the result
                metadata = result.get("metadata", {})

                # Create content chunk with enhanced source information
                content_chunk = ContentChunk(
                    text=content_text,
                    source_reference=source_reference,
                    relevance_score=relevance_score
                )

                # Enhance the content chunk with additional source information
                # For now, we'll add it to the source reference field
                if metadata and isinstance(metadata, dict):
                    if "page_number" in metadata:
                        content_chunk.source_reference += f" (Page: {metadata['page_number']})"
                    if "chapter" in metadata:
                        content_chunk.source_reference += f" (Chapter: {metadata['chapter']})"
                    if "section_title" in metadata:
                        content_chunk.source_reference += f" (Section: {metadata['section_title']})"

                content_chunks.append(content_chunk)

            # Create retrieval metadata
            retrieval_metadata = RetrievalMetadata(
                retrieval_method="selected_text_similarity",
                confidence_score=filtered_results[0]["relevance_score"] if filtered_results else 0.0,
                timestamp=datetime.now()
            )

            # Create retrieved context object
            retrieved_context = RetrievedContext(
                context_id=UUID(str(query.query_id)),  # Using query ID as context ID for now
                query_id=query.query_id,
                content_chunks=content_chunks,
                metadata=retrieval_metadata
            )

            return retrieved_context

        except Exception as e:
            logger.error(f"Error in retrieve_context_for_selected_text: {e}")
            return None

    def retrieve_context_by_type(self, query: Query, top_k: int = 5) -> Optional[RetrievedContext]:
        """
        Retrieve context based on the query's context type
        """
        if query.context_type == ContextType.FULL_BOOK:
            return self.retrieve_context(query, top_k)
        elif query.context_type == ContextType.SELECTED_TEXT and query.selected_text:
            return self.retrieve_context_for_selected_text(query, top_k)
        else:
            # Default to full book context
            return self.retrieve_context(query, top_k)

    def validate_retrieved_context(self, retrieved_context: RetrievedContext, min_chunks: int = 1) -> bool:
        """
        Validate that the retrieved context meets quality requirements
        """
        if not retrieved_context or not retrieved_context.content_chunks:
            logger.warning("Retrieved context has no content chunks")
            return False

        if len(retrieved_context.content_chunks) < min_chunks:
            logger.warning(f"Retrieved context has fewer chunks than required: {len(retrieved_context.content_chunks)} < {min_chunks}")
            return False

        # Check if the average relevance score is above a threshold
        avg_relevance = sum(chunk.relevance_score or 0 for chunk in retrieved_context.content_chunks) / len(retrieved_context.content_chunks)
        if avg_relevance < 0.1:  # Threshold can be adjusted
            logger.warning(f"Retrieved context has low average relevance: {avg_relevance}")
            return False

        return True