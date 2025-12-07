from typing import List, Tuple
import re
from uuid import UUID, uuid4
from chatbot.core.models.book_content import BookContent, ContentMetadata


class TextChunker:
    """Utility class for chunking text content into smaller pieces for embedding"""

    @staticmethod
    def chunk_by_tokens(text: str, max_tokens: int = 512, overlap: int = 50) -> List[str]:
        """
        Chunk text based on token count (approximated by word count)
        """
        # Simple tokenization by words (in a real implementation, you might use a proper tokenizer)
        words = text.split()
        chunks = []

        start_idx = 0
        while start_idx < len(words):
            end_idx = start_idx + max_tokens
            chunk_words = words[start_idx:end_idx]
            chunk = " ".join(chunk_words)

            chunks.append(chunk)

            # Move start index forward by max_tokens minus overlap
            start_idx = end_idx - overlap if end_idx < len(words) else len(words)

        return chunks

    @staticmethod
    def chunk_by_sentences(text: str, max_sentences: int = 3, overlap: int = 1) -> List[str]:
        """
        Chunk text based on sentence count
        """
        # Split text into sentences using regex
        sentence_endings = r'[.!?]+(?:\s|$)'
        sentences = re.split(sentence_endings, text)
        # Remove empty strings
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        start_idx = 0

        while start_idx < len(sentences):
            end_idx = start_idx + max_sentences
            chunk_sentences = sentences[start_idx:end_idx]
            chunk = ". ".join([s for s in chunk_sentences if s]) + "."

            chunks.append(chunk)

            # Move start index forward
            start_idx = end_idx - overlap if end_idx < len(sentences) else len(sentences)

        return chunks

    @staticmethod
    def chunk_by_paragraphs(text: str, max_paragraphs: int = 2, overlap: int = 0) -> List[str]:
        """
        Chunk text based on paragraph count
        """
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []

        start_idx = 0
        while start_idx < len(paragraphs):
            end_idx = start_idx + max_paragraphs
            chunk_paragraphs = paragraphs[start_idx:end_idx]
            chunk = "\n\n".join(chunk_paragraphs)

            chunks.append(chunk)

            # Move start index forward
            start_idx = end_idx - overlap if end_idx < len(paragraphs) else len(paragraphs)

        return chunks

    @staticmethod
    def chunk_with_semantic_boundaries(text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Chunk text respecting semantic boundaries (paragraphs, sentences)
        """
        chunks = []

        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        current_chunk = ""

        for paragraph in paragraphs:
            # If adding this paragraph would exceed the limit
            if len(current_chunk) + len(paragraph) > max_chunk_size:
                # If current chunk is substantial, save it
                if len(current_chunk) > max_chunk_size // 4:  # At least 25% of max size
                    chunks.append(current_chunk.strip())
                    # Start new chunk with overlap if possible
                    if overlap > 0 and len(paragraph) < max_chunk_size:
                        # Use end of current chunk as overlap
                        overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                        current_chunk = overlap_text + "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    # Current chunk is small, try to fit more content
                    if len(paragraph) <= max_chunk_size:
                        current_chunk += "\n\n" + paragraph
                    else:
                        # Paragraph is too big, need to further split it
                        sub_chunks = TextChunker.chunk_by_sentences(paragraph, max_sentences=3, overlap=1)
                        for sub_chunk in sub_chunks:
                            if len(sub_chunk) <= max_chunk_size:
                                if current_chunk and len(current_chunk) + len(sub_chunk) <= max_chunk_size:
                                    current_chunk += "\n\n" + sub_chunk
                                    chunks.append(current_chunk.strip())
                                    current_chunk = ""
                                else:
                                    if current_chunk:
                                        chunks.append(current_chunk.strip())
                                    chunks.append(sub_chunk.strip())
                                    current_chunk = ""
                            else:
                                # If sub-chunk is still too big, split by tokens
                                token_chunks = TextChunker.chunk_by_tokens(sub_chunk, max_tokens=512, overlap=50)
                                for token_chunk in token_chunks:
                                    chunks.append(token_chunk.strip())
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Filter out very small chunks
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 20]

        return chunks

    @staticmethod
    def chunk_book_content(book_content: BookContent, max_chunk_size: int = 1000, overlap: int = 100) -> List[BookContent]:
        """
        Chunk a BookContent object into multiple BookContent objects
        """
        text = book_content.content_text
        source_ref_base = book_content.source_reference

        text_chunks = TextChunker.chunk_with_semantic_boundaries(text, max_chunk_size, overlap)

        chunked_contents = []
        for i, chunk_text in enumerate(text_chunks):
            chunk = BookContent(
                content_id=uuid4(),
                book_id=book_content.book_id,
                title=f"{book_content.title} - Part {i+1}",
                content_text=chunk_text,
                metadata=ContentMetadata(
                    chapter_number=book_content.metadata.chapter_number,
                    page_number=book_content.metadata.page_number,
                    section_title=f"{book_content.metadata.section_title} - Part {i+1}",
                    tags=book_content.metadata.tags + [f"chunk-{i+1}"],
                    created_at=book_content.metadata.created_at
                ),
                source_reference=f"{source_ref_base}#part-{i+1}"
            )
            chunked_contents.append(chunk)

        return chunked_contents