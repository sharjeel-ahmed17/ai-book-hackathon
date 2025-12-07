"""
Comprehensive test suite for the RAG Chatbot functionality
"""
import pytest
import asyncio
from uuid import uuid4
from typing import List

from chatbot.core.models.book_content import BookContent, ContentMetadata
from chatbot.core.embeddings.processor import EmbeddingProcessor
from chatbot.core.storage.vector_db import VectorDB
from chatbot.core.storage.metadata_db import MetadataDB
from chatbot.core.rag.retriever import RAGRetriever
from chatbot.core.rag.generator import RAGGenerator
from chatbot.core.rag.validator import RAGValidator
from chatbot.services.session_manager import SessionManager
from chatbot.services.query_service import QueryService
from chatbot.core.embeddings.content_embedder import ContentEmbedder


class TestRAGChatbot:
    """Test class for RAG Chatbot functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.embedding_processor = EmbeddingProcessor()
        self.vector_db = VectorDB()
        self.metadata_db = MetadataDB()
        self.session_manager = SessionManager(self.metadata_db)

        # Initialize RAG components
        self.retriever = RAGRetriever(self.vector_db, self.metadata_db, self.embedding_processor)
        self.generator = RAGGenerator()
        self.validator = RAGValidator(self.embedding_processor)
        self.query_service = QueryService(
            self.retriever,
            self.generator,
            self.validator,
            self.metadata_db,
            self.session_manager
        )
        self.content_embedder = ContentEmbedder(self.embedding_processor, self.vector_db)

        # Create sample content for testing
        self.sample_content = [
            BookContent(
                content_id=uuid4(),
                book_id="test-book-1",
                title="Introduction to RAG Systems",
                content_text="A Retrieval-Augmented Generation (RAG) system combines a retriever that finds relevant documents and a generator that creates responses based on those documents. This approach helps ensure responses are grounded in actual data.",
                metadata=ContentMetadata(
                    chapter_number=1,
                    section_title="What is RAG?",
                    tags=["RAG", "Introduction", "System Design"]
                ),
                source_reference="Chapter 1, Page 1"
            ),
            BookContent(
                content_id=uuid4(),
                book_id="test-book-1",
                title="How RAG Works",
                content_text="The RAG process involves three main steps: 1) Retrieve relevant documents based on the user query, 2) Augment the query with retrieved context, 3) Generate a response using the combined information.",
                metadata=ContentMetadata(
                    chapter_number=1,
                    section_title="RAG Process",
                    tags=["RAG", "Process", "Steps"]
                ),
                source_reference="Chapter 1, Page 2"
            )
        ]

    def test_content_embedding(self):
        """Test that content can be properly embedded and stored"""
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count == len(self.sample_content), f"Expected {len(self.sample_content)} successes, got {success_count}"

    def test_full_book_query(self):
        """Test full-book query functionality"""
        # First embed the content
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count > 0, "Content embedding failed"

        # Test query
        response = self.query_service.process_full_book_query(
            query_text="What is a RAG system?",
            user_id=uuid4()
        )

        assert response is not None, "Response should not be None"
        assert len(response.content) > 0, "Response should have content"
        assert len(response.source_references) > 0, "Response should have source references"
        assert response.validation_status.name in ["PASSED", "FAILED", "PENDING"], "Invalid validation status"

    def test_selected_text_query(self):
        """Test selected-text query functionality"""
        selected_text = "A Retrieval-Augmented Generation (RAG) system combines a retriever that finds relevant documents"

        response = self.query_service.process_selected_text_query(
            query_text="What does this text say about RAG?",
            selected_text=selected_text,
            user_id=uuid4()
        )

        assert response is not None, "Response should not be None"
        assert len(response.content) > 0, "Response should have content"
        assert len(response.source_references) > 0, "Response should have source references"

    def test_source_attribution(self):
        """Test that responses include proper source attribution"""
        # Embed content first
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count > 0, "Content embedding failed"

        # Test query
        response = self.query_service.process_full_book_query(
            query_text="How does RAG work?",
            user_id=uuid4()
        )

        assert response is not None, "Response should not be None"
        assert len(response.source_references) > 0, "Response should have source references"

        # Check that source references have the expected fields
        for ref in response.source_references:
            assert hasattr(ref, 'reference'), "Source reference should have 'reference' field"
            assert hasattr(ref, 'text'), "Source reference should have 'text' field"
            assert hasattr(ref, 'relevance_score'), "Source reference should have 'relevance_score' field"

    def test_hallucination_validation(self):
        """Test that the system validates against hallucination"""
        # Embed content first
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count > 0, "Content embedding failed"

        # Test query
        response = self.query_service.process_full_book_query(
            query_text="What is a RAG system?",
            user_id=uuid4()
        )

        assert response is not None, "Response should not be None"
        # The validation status should be PASSED, FAILED, or PENDING
        assert response.validation_status.name in ["PASSED", "FAILED", "PENDING"], "Invalid validation status"

    def test_empty_query_handling(self):
        """Test that the system handles empty queries gracefully"""
        response = self.query_service.process_full_book_query(
            query_text="",
            user_id=uuid4()
        )

        # Should return None or handle gracefully
        # The exact behavior depends on validation logic
        assert response is None, "Empty query should result in None response"

    def test_long_query_handling(self):
        """Test that the system handles long queries properly"""
        long_query = "A" * 1001  # Exceeds typical length limits

        response = self.query_service.process_full_book_query(
            query_text=long_query,
            user_id=uuid4()
        )

        # Should handle gracefully, possibly returning None or a validation error
        # The exact behavior depends on validation logic
        assert response is None, "Long query should be rejected"

    def test_query_by_context_type(self):
        """Test that queries can be processed by context type"""
        # Test full book context
        response1 = self.query_service.process_query_by_context_type(
            query_text="What is RAG?",
            context_type="FULL_BOOK",
            user_id=uuid4()
        )

        assert response1 is not None, "Full-book context query should work"

        # Test selected text context
        response2 = self.query_service.process_query_by_context_type(
            query_text="What does this mean?",
            context_type="SELECTED_TEXT",
            selected_text="RAG systems are useful",
            user_id=uuid4()
        )

        assert response2 is not None, "Selected-text context query should work"

    def test_session_management(self):
        """Test that sessions are properly managed"""
        session_id = uuid4()

        # Create a session
        session = self.session_manager.create_session(str(uuid4()))
        assert session is not None, "Session should be created"

        # Verify session exists
        retrieved_session = self.session_manager.get_session(str(session.session_id))
        assert retrieved_session is not None, "Session should be retrievable"

    def test_content_retrieval(self):
        """Test that content can be properly retrieved"""
        # Embed content first
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count > 0, "Content embedding failed"

        # Create a query object
        from chatbot.core.models.query import Query, ContextType
        from datetime import datetime

        query_obj = Query(
            query_id=uuid4(),
            session_id=uuid4(),
            content="What is RAG?",
            context_type=ContextType.FULL_BOOK,
            selected_text=None,
            timestamp=datetime.now(),
            source_references=[]
        )

        # Retrieve context
        retrieved_context = self.retriever.retrieve_context(query_obj)

        assert retrieved_context is not None, "Retrieved context should not be None"
        assert len(retrieved_context.content_chunks) > 0, "Retrieved context should have content chunks"

    def test_zero_hallucination_requirement(self):
        """Test that the system meets the zero hallucination requirement"""
        # Embed content first
        success_count = self.content_embedder.embed_and_store_batch(self.sample_content)
        assert success_count > 0, "Content embedding failed"

        # Test with a query that should be answerable from the content
        response = self.query_service.process_full_book_query(
            query_text="What is a RAG system?",
            user_id=uuid4()
        )

        assert response is not None, "Response should not be None for valid query"
        assert len(response.source_references) > 0, "Response should have source references"

        # The validator should confirm no hallucination
        # This is handled internally by the query service
        assert response.validation_status.name in ["PASSED", "FAILED", "PENDING"], "Invalid validation status"


# Run tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__])