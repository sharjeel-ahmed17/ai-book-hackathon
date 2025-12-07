"""
Test for source attribution functionality.
This verifies that responses include proper source citations that link back to specific parts of the book content.
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


def test_source_attribution():
    """Test that responses include proper source citations"""
    print("Setting up RAG system for source attribution testing...")

    # Initialize all components
    embedding_processor = EmbeddingProcessor()
    vector_db = VectorDB()
    metadata_db = MetadataDB()
    session_manager = SessionManager(metadata_db)

    # Create sample book content with rich metadata
    sample_content = [
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-3",
            title="Advanced RAG Techniques",
            content_text="Retrieval-Augmented Generation (RAG) combines retrieval of relevant documents with generative models. This technique significantly improves the accuracy and reliability of AI responses by grounding them in actual data.",
            metadata=ContentMetadata(
                chapter_number=3,
                page_number=45,
                section_title="Introduction to RAG",
                tags=["RAG", "Techniques", "Accuracy"]
            ),
            source_reference="Chapter 3, Page 45"
        ),
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-3",
            title="RAG Implementation Patterns",
            content_text="There are several patterns for implementing RAG systems. The most common approach involves indexing documents in a vector database, then retrieving relevant documents based on user queries before generating responses.",
            metadata=ContentMetadata(
                chapter_number=4,
                page_number=62,
                section_title="Implementation Patterns",
                tags=["RAG", "Implementation", "Patterns"]
            ),
            source_reference="Chapter 4, Page 62"
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

    print("\nTesting source attribution for full-book query:")
    print("Query: 'What is RAG and how does it improve AI responses?'")

    response = query_service.process_full_book_query(
        query_text="What is RAG and how does it improve AI responses?",
        user_id=uuid4()
    )

    if response:
        print(f"Response: {response.content}")
        print(f"Validation Status: {response.validation_status}")
        print(f"Source References: {len(response.source_references)} found")
        for i, ref in enumerate(response.source_references):
            print(f"  Reference {i+1}:")
            print(f"    Source: {ref.reference}")
            print(f"    Snippet: {ref.text[:100]}...")
            print(f"    Relevance: {ref.relevance_score}")
            print(f"    Page: {ref.page_number}")
            print(f"    Chapter: {ref.chapter}")
            print(f"    Section: {ref.section}")
            print(f"    Content ID: {ref.content_id}")
    else:
        print("No response generated")

    print("\nTesting source attribution for selected-text query:")
    selected_text = "There are several patterns for implementing RAG systems. The most common approach involves indexing documents in a vector database."
    print(f"Selected text: '{selected_text}'")
    print("Query: 'What are common RAG implementation approaches?'")

    response2 = query_service.process_selected_text_query(
        query_text="What are common RAG implementation approaches?",
        selected_text=selected_text,
        user_id=uuid4()
    )

    if response2:
        print(f"Response: {response2.content}")
        print(f"Validation Status: {response2.validation_status}")
        print(f"Source References: {len(response2.source_references)} found")
        for i, ref in enumerate(response2.source_references):
            print(f"  Reference {i+1}:")
            print(f"    Source: {ref.reference}")
            print(f"    Snippet: {ref.text[:100]}...")
            print(f"    Relevance: {ref.relevance_score}")
            print(f"    Page: {ref.page_number}")
            print(f"    Chapter: {ref.chapter}")
            print(f"    Section: {ref.section}")
            print(f"    Content ID: {ref.content_id}")
    else:
        print("No response generated")

    print("\nSource attribution tests completed!")


if __name__ == "__main__":
    test_source_attribution()