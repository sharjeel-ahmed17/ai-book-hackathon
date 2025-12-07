from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
import re
from markdown import markdown
from bs4 import BeautifulSoup
from chatbot.core.models.book_content import BookContent, ContentMetadata


class ContentConverter:
    """Utility class for converting various content formats to BookContent models"""

    @staticmethod
    def convert_from_markdown(content: str, book_id: str, title: str = "", source_reference: str = "") -> List[BookContent]:
        """
        Convert markdown content to BookContent models
        Splits content into chunks based on headers and paragraphs
        """
        chunks = []

        # Convert markdown to HTML for easier parsing
        html_content = markdown(content)

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract text by sections (h1, h2, h3 tags)
        sections = []
        current_section = {"title": title, "content": "", "source_ref": source_reference}

        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote']):
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)

                # Start new section
                current_section = {
                    "title": element.get_text().strip(),
                    "content": "",
                    "source_ref": f"{source_reference}#{element.name}-{element.get_text().strip()[:50]}"
                }
            elif element.name in ['p', 'li', 'blockquote']:
                text = element.get_text().strip()
                if text:
                    current_section["content"] += text + "\n\n"

        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)

        # Convert sections to BookContent models
        for i, section in enumerate(sections):
            chunk = BookContent(
                content_id=uuid4(),
                book_id=book_id,
                title=section["title"],
                content_text=section["content"],
                metadata=ContentMetadata(
                    section_title=section["title"],
                    tags=["markdown"]
                ),
                source_reference=section["source_ref"]
            )
            chunks.append(chunk)

        return chunks

    @staticmethod
    def convert_from_text(content: str, book_id: str, title: str = "", source_reference: str = "",
                         max_chunk_size: int = 1000, overlap: int = 100) -> List[BookContent]:
        """
        Convert plain text content to BookContent models
        Splits content into overlapping chunks to maintain context
        """
        chunks = []

        # Split content into sentences to avoid cutting in the middle of sentences
        sentences = re.split(r'[.!?]+', content)

        current_chunk = ""
        current_pos = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + ". "
            else:
                # Save current chunk
                if current_chunk.strip():
                    chunk = BookContent(
                        content_id=uuid4(),
                        book_id=book_id,
                        title=f"{title} - Chunk {len(chunks) + 1}",
                        content_text=current_chunk.strip(),
                        metadata=ContentMetadata(
                            tags=["text", f"chunk-{len(chunks) + 1}"]
                        ),
                        source_reference=f"{source_reference}#chunk-{len(chunks) + 1}"
                    )
                    chunks.append(chunk)

                # Start new chunk with some overlap
                if overlap > 0 and len(sentence) < max_chunk_size:
                    # Find a reasonable overlap point
                    overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                    current_chunk = overlap_text + " " + sentence + ". "
                else:
                    current_chunk = sentence + ". "

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk = BookContent(
                content_id=uuid4(),
                book_id=book_id,
                title=f"{title} - Chunk {len(chunks) + 1}",
                content_text=current_chunk.strip(),
                metadata=ContentMetadata(
                    tags=["text", f"chunk-{len(chunks) + 1}"]
                ),
                source_reference=f"{source_reference}#chunk-{len(chunks) + 1}"
            )
            chunks.append(chunk)

        return chunks

    @staticmethod
    def convert_from_html(content: str, book_id: str, title: str = "", source_reference: str = "") -> List[BookContent]:
        """
        Convert HTML content to BookContent models
        Extracts content by semantic sections
        """
        chunks = []
        soup = BeautifulSoup(content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Find main content containers
        content_containers = soup.find_all(['div', 'section', 'article', 'main'])

        if not content_containers:
            # If no semantic containers found, just get the body
            body = soup.find('body') or soup
            text = body.get_text()
            if text.strip():
                chunk = BookContent(
                    content_id=uuid4(),
                    book_id=book_id,
                    title=title,
                    content_text=text,
                    metadata=ContentMetadata(tags=["html"]),
                    source_reference=source_reference
                )
                chunks.append(chunk)
        else:
            for i, container in enumerate(content_containers):
                text = container.get_text(separator=' ', strip=True)
                if text and len(text) > 50:  # Only include substantial content
                    chunk_title = container.find(['h1', 'h2', 'h3', 'h4'])
                    chunk_title = chunk_title.get_text().strip() if chunk_title else f"{title} - Section {i+1}"

                    chunk = BookContent(
                        content_id=uuid4(),
                        book_id=book_id,
                        title=chunk_title,
                        content_text=text,
                        metadata=ContentMetadata(
                            tags=["html", f"section-{i+1}"]
                        ),
                        source_reference=f"{source_reference}#section-{i+1}"
                    )
                    chunks.append(chunk)

        return chunks

    @staticmethod
    def convert_from_json_structure(data: Dict[str, Any], book_id: str) -> List[BookContent]:
        """
        Convert structured JSON data to BookContent models
        Expects format like: {"chapters": [{"title": "...", "content": "..."}, ...]}
        """
        chunks = []

        # Handle different JSON structures
        if "chapters" in data:
            for i, chapter in enumerate(data["chapters"]):
                if "content" in chapter:
                    chunk = BookContent(
                        content_id=uuid4(),
                        book_id=book_id,
                        title=chapter.get("title", f"Chapter {i+1}"),
                        content_text=chapter["content"],
                        metadata=ContentMetadata(
                            chapter_number=i+1,
                            section_title=chapter.get("title", ""),
                            tags=["json", "chapter"]
                        ),
                        source_reference=f"json://book/{book_id}/chapter/{i+1}"
                    )
                    chunks.append(chunk)
        elif "pages" in data:
            for i, page in enumerate(data["pages"]):
                if "content" in page or "text" in page:
                    content = page.get("content", page.get("text", ""))
                    chunk = BookContent(
                        content_id=uuid4(),
                        book_id=book_id,
                        title=page.get("title", f"Page {i+1}"),
                        content_text=content,
                        metadata=ContentMetadata(
                            page_number=i+1,
                            tags=["json", "page"]
                        ),
                        source_reference=f"json://book/{book_id}/page/{i+1}"
                    )
                    chunks.append(chunk)
        elif "content" in data:
            # Single content block
            chunk = BookContent(
                content_id=uuid4(),
                book_id=book_id,
                title=data.get("title", "Book Content"),
                content_text=data["content"],
                metadata=ContentMetadata(
                    tags=["json", "single-block"]
                ),
                source_reference=f"json://book/{book_id}/content"
            )
            chunks.append(chunk)

        return chunks