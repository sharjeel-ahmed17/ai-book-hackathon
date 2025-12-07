from typing import List, Optional
import cohere
import google.generativeai as genai
from openai import OpenAI
from chatbot.config.settings import settings
import logging


logger = logging.getLogger(__name__)


class EmbeddingProcessor:
    def __init__(self):
        self.cohere_client = None
        self.openai_client = None
        self.gemini_client = None

        # Initialize clients if API keys are available
        if settings.cohere_api_key:
            self.cohere_client = cohere.Client(settings.cohere_api_key)

        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_client = genai

    def generate_embedding(self, text: str, model: str = "embed-english-v3.0") -> Optional[List[float]]:
        """Generate embedding for the given text using the specified model"""
        if self.cohere_client:
            try:
                response = self.cohere_client.embed(
                    texts=[text],
                    model=model,
                    input_type="search_query"  # or "search_document" for content
                )
                return response.embeddings[0]  # Return the first embedding
            except Exception as e:
                logger.error(f"Error generating embedding with Cohere: {e}")

        # Fallback to OpenAI if available
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=text,
                    model="text-embedding-ada-002"  # or another embedding model
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"Error generating embedding with OpenAI: {e}")

        # If no clients are available, return None
        logger.warning("No embedding client available")
        return None

    def generate_embeddings_batch(self, texts: List[str], model: str = "embed-english-v3.0") -> Optional[List[List[float]]]:
        """Generate embeddings for a batch of texts"""
        if self.cohere_client:
            try:
                response = self.cohere_client.embed(
                    texts=texts,
                    model=model,
                    input_type="search_document"  # For document embeddings
                )
                return response.embeddings
            except Exception as e:
                logger.error(f"Error generating batch embeddings with Cohere: {e}")

        # Fallback to OpenAI if available
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=texts,
                    model="text-embedding-ada-002"
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                logger.error(f"Error generating batch embeddings with OpenAI: {e}")

        logger.warning("No embedding client available for batch processing")
        return None

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        import numpy as np
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))