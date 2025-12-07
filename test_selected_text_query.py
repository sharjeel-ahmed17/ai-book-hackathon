"""
Test for selected-text query functionality.
This demonstrates how the RAG system handles queries with specific text selections.
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


def test_selected_text_query():
    """Test the selected-text query functionality"""
    print("Setting up RAG system for selected-text testing...")

    # Initialize all components
    embedding_processor = EmbeddingProcessor()
    vector_db = VectorDB()
    metadata_db = MetadataDB()
    session_manager = SessionManager(metadata_db)

    # Create sample book content
    sample_content = [
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-2",
            title="Introduction to Machine Learning",
            content_text="Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.",
            metadata=ContentMetadata(
                chapter_number=1,
                section_title="What is Machine Learning?",
                tags=["ML", "Introduction", "AI"]
            ),
            source_reference="Chapter 1, Page 1"
        ),
        BookContent(
            content_id=uuid4(),
            book_id="sample-book-2",
            title="Types of Machine Learning",
            content_text="There are three main types of machine learning: supervised learning, where the model is trained on labeled data; unsupervised learning, where the model finds patterns in unlabeled data; and reinforcement learning, where the model learns through trial and error.",
            metadata=ContentMetadata(
                chapter_number=2,
                section_title="ML Types",
                tags=["ML", "Types", "Supervised", "Unsupervised", "Reinforcement"]
            ),
            source_reference="Chapter 2, Page 1"
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

    # Test 1: Query with selected text
    selected_text = "Machine learning is a method of data analysis that automates analytical model building."
    print(f"\nTesting query with selected text: '{selected_text}'")
    print("Query: 'What does this text say about machine learning?'")

    response = query_service.process_selected_text_query(
        query_text="What does this text say about machine learning?",
        selected_text=selected_text,
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

    # Test 2: Another selected text query
    selected_text2 = "There are three main types of machine learning: supervised learning, where the model is trained on labeled data; unsupervised learning, where the model finds patterns in unlabeled data; and reinforcement learning, where the model learns through trial and error."
    print(f"\nTesting query with selected text: '{selected_text2[:100]}...'")
    print("Query: 'What are the three main types of machine learning?'")

    response2 = query_service.process_selected_text_query(
        query_text="What are the three main types of machine learning?",
        selected_text=selected_text2,
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

    print("\nSelected-text query tests completed!")


if __name__ == "__main__":
    test_selected_text_query()