"""
Sample test for full-book query functionality.
This demonstrates how the RAG system would work with sample content.
"""
import asyncio
from uuid import uuid4
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


def test_full_book_query():
    """Test the full-book query functionality with sample content"""
    print("Setting up RAG system for testing...")

    # Initialize all components
    embedding_processor = EmbeddingProcessor()
    vector_db = VectorDB()
    metadata_db = MetadataDB()
    session_manager = SessionManager(metadata_db)

    # Create sample book content
    sample_content = [
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-1",
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
            book_id="sample-book-1",
            title="How RAG Works",
            content_text="The RAG process involves three main steps: 1) Retrieve relevant documents based on the user query, 2) Augment the query with retrieved context, 3) Generate a response using the combined information.",
            metadata=ContentMetadata(
                chapter_number=1,
                section_title="RAG Process",
                tags=["RAG", "Process", "Steps"]
            ),
            source_reference="Chapter 1, Page 2"
        ),
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-1",
            title="Benefits of RAG",
            content_text="RAG systems provide several benefits including improved accuracy, reduced hallucination, and the ability to incorporate up-to-date information without retraining the entire model.",
            metadata=ContentMetadata(
                chapter_number=1,
                section_title="Benefits",
                tags=["RAG", "Benefits", "Accuracy"]
            ),
            source_reference="Chapter 1, Page 3"
        )
    ]

    print("Embedding sample content...")
    content_embedder = ContentEmbedder(embedding_processor, vector_db)
    success_count = content_embedder.embed_and_store_batch(sample_content)
    print(f"Successfully embedded {success_count} out of {len(sample_content)} content pieces")

    # Initialize RAG components
    retriever = RAGRetriever(vector_db, metadata_db, embedding_processor)
    generator = RAGGenerator()
    validator = RAGValidator(embedding_processor)

    # Create query service
    query_service = QueryService(retriever, generator, validator, metadata_db, session_manager)

    print("\nTesting query: 'What is a RAG system?'")
    response = query_service.process_full_book_query(
        query_text="What is a RAG system?",
        user_id=uuid4()
    )

    if response:
        print(f"Response: {response.content}")
        print(f"Validation Status: {response.validation_status}")
        print(f"Source References: {len(response.source_references)} found")
        for i, ref in enumerate(response.source_references):
            print(f"  Reference {i+1}: {ref.reference}")
            print(f"    Snippet: {ref.text[:100]}...")
    else:
        print("No response generated")

    print("\nTesting query: 'What are the benefits of RAG systems?'")
    response2 = query_service.process_full_book_query(
        query_text="What are the benefits of RAG systems?",
        user_id=uuid4()
    )

    if response2:
        print(f"Response: {response2.content}")
        print(f"Validation Status: {response2.validation_status}")
        print(f"Source References: {len(response2.source_references)} found")
        for i, ref in enumerate(response2.source_references):
            print(f"  Reference {i+1}: {ref.reference}")
    else:
        print("No response generated")

    print("\nTest completed!")


if __name__ == "__main__":
    test_full_book_query()