from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
import logging
import openai
import google.generativeai as genai
from chatbot.config.settings import settings
from chatbot.core.models.response import Response, ValidationStatus, SourceReference
from chatbot.core.models.retrieved_context import RetrievedContext
from chatbot.core.models.query import Query
from chatbot.utils.validators import ResponseValidator


logger = logging.getLogger(__name__)


class RAGGenerator:
    """Generates responses based on retrieved context and user queries"""

    def __init__(self):
        self.openai_client = None
        self.gemini_model = None

        # Initialize clients if API keys are available
        if settings.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)

        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, query: Query, retrieved_context: RetrievedContext) -> Optional[Response]:
        """
        Generate a response based on the query and retrieved context
        """
        try:
            # Format the prompt with retrieved context
            context_texts = [chunk.text for chunk in retrieved_context.content_chunks]
            context_str = "\n\n".join(context_texts)

            # Create the prompt for the LLM
            prompt = self._create_prompt(query.content, context_str)

            # Generate response using available LLM
            response_text = self._generate_with_llm(prompt)

            if not response_text:
                logger.error("Failed to generate response from LLM")
                return None

            # Extract source references from the retrieved context
            source_references = []
            for chunk in retrieved_context.content_chunks:
                # Try to extract additional metadata from the source reference
                page_number = None
                chapter = None
                section = None

                # Simple parsing of source reference to extract metadata
                if "page" in chunk.source_reference.lower():
                    import re
                    page_match = re.search(r'page\s*(\d+)', chunk.source_reference, re.IGNORECASE)
                    if page_match:
                        page_number = int(page_match.group(1))

                if "chapter" in chunk.source_reference.lower():
                    import re
                    chapter_match = re.search(r'chapter\s*([^\s,/#]+)', chunk.source_reference, re.IGNORECASE)
                    if chapter_match:
                        chapter = chapter_match.group(1)

                if "section" in chunk.source_reference.lower():
                    import re
                    section_match = re.search(r'section\s*([^\s,/#]+)', chunk.source_reference, re.IGNORECASE)
                    if section_match:
                        section = section_match.group(1)

                source_ref = SourceReference(
                    reference=chunk.source_reference,
                    text=chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,  # Truncate for response
                    relevance_score=chunk.relevance_score,
                    page_number=page_number,
                    chapter=chapter,
                    section=section,
                    content_id=str(retrieved_context.context_id)  # Using context_id as content_id for this example
                )
                source_references.append(source_ref)

            # Create the response object
            response = Response(
                response_id=uuid4(),
                query_id=query.query_id,
                content=response_text,
                source_references=source_references,
                timestamp=datetime.now(),
                validation_status=ValidationStatus.PENDING  # Will be validated separately
            )

            return response

        except Exception as e:
            logger.error(f"Error in generate_response: {e}")
            return None

    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create a prompt for the LLM with the query and context
        """
        prompt = f"""
        You are a helpful assistant that answers questions based only on the provided context.
        Your answers must be grounded in the provided context and you should not hallucinate information.
        If the answer cannot be found in the context, please say so.

        Context:
        {context}

        Question: {query}

        Answer:
        """
        return prompt.strip()

    def _generate_with_llm(self, prompt: str) -> Optional[str]:
        """
        Generate text using the available LLM (OpenAI or Gemini)
        """
        # Try OpenAI first if available
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context. Your answers must be grounded in the provided context and you should not hallucinate information. If the answer cannot be found in the context, please say so."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Error generating with OpenAI: {e}")

        # Fallback to Gemini if available
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 500,
                        "temperature": 0.3
                    }
                )
                return response.text.strip()
            except Exception as e:
                logger.error(f"Error generating with Gemini: {e}")

        logger.error("No LLM client available for response generation")
        return None

    def generate_response_with_selected_text_context(self, query: Query, selected_text: str) -> Optional[Response]:
        """
        Generate a response specifically for selected text queries
        """
        try:
            # Create the prompt with selected text as the primary context
            prompt = f"""
            You are a helpful assistant that answers questions based only on the provided selected text.
            Your answers must be grounded in the provided selected text and you should not hallucinate information.
            If the answer cannot be found in the selected text, please say so.

            Selected Text:
            {selected_text}

            Question: {query.content}

            Answer:
            """

            # Generate response using available LLM
            response_text = self._generate_with_llm(prompt)

            if not response_text:
                logger.error("Failed to generate response from LLM for selected text query")
                return None

            # Create a source reference from the selected text
            source_references = [
                SourceReference(
                    reference="Selected Text Provided by User",
                    text=selected_text[:200] + "..." if len(selected_text) > 200 else selected_text,
                    relevance_score=1.0,
                    page_number=None,
                    chapter=None,
                    section=None,
                    content_id=None
                )
            ]

            # Create the response object
            response = Response(
                response_id=uuid4(),
                query_id=query.query_id,
                content=response_text,
                source_references=source_references,
                timestamp=datetime.now(),
                validation_status=ValidationStatus.PENDING  # Will be validated separately
            )

            return response

        except Exception as e:
            logger.error(f"Error in generate_response_with_selected_text_context: {e}")
            return None

    def validate_response_content(self, response: Response, retrieved_context: RetrievedContext) -> ValidationStatus:
        """
        Validate that the response is grounded in the retrieved context
        """
        try:
            # Use the ResponseValidator to check basic response validity
            content_errors = ResponseValidator.validate_response_content(response.content)
            attribution_errors = ResponseValidator.validate_source_attribution(response.source_references)

            if content_errors or attribution_errors:
                logger.warning(f"Response validation failed: {content_errors + attribution_errors}")
                return ValidationStatus.FAILED

            # Additional check: ensure the response references information from the context
            response_lower = response.content.lower()
            context_texts = [chunk.text.lower() for chunk in retrieved_context.content_chunks]

            # Check if response contains information from context (basic heuristic)
            context_mentioned = any(any(word in response_lower for word in chunk.split()[:10])
                                  for chunk in context_texts if len(chunk.split()) > 10)

            if not context_mentioned and len([c for c in context_texts if c]) > 0:
                logger.warning("Response may not be properly grounded in context")
                return ValidationStatus.FAILED

            return ValidationStatus.PASSED

        except Exception as e:
            logger.error(f"Error in validate_response_content: {e}")
            return ValidationStatus.FAILED