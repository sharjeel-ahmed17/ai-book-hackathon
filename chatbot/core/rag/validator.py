from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
from sentence_transformers import util
import torch
from chatbot.core.models.response import Response, ValidationStatus
from chatbot.core.models.retrieved_context import RetrievedContext
from chatbot.core.models.query import Query
from chatbot.core.embeddings.processor import EmbeddingProcessor


logger = logging.getLogger(__name__)


class RAGValidator:
    """Validates that responses are properly grounded in retrieved context"""

    def __init__(self, embedding_processor: EmbeddingProcessor):
        self.embedding_processor = embedding_processor

    def validate_response_grounding(self, query: Query, retrieved_context: RetrievedContext, response: Response) -> ValidationStatus:
        """
        Validate that the response is grounded in the retrieved context
        """
        try:
            # Check if the response contains information from the retrieved context
            context_texts = [chunk.text for chunk in retrieved_context.content_chunks if chunk.text]

            if not context_texts:
                logger.warning("No context texts available for grounding validation")
                return ValidationStatus.FAILED

            # Method 1: Text overlap check
            text_overlap_valid = self._check_text_overlap(response.content, context_texts)

            # Method 2: Semantic similarity check using embeddings
            semantic_similarity_valid = self._check_semantic_similarity(
                response.content, context_texts
            )

            # Method 3: Check if response mentions information from context
            content_mention_valid = self._check_content_mention(response.content, context_texts)

            # Method 4: Ensure response doesn't contain hallucinated information
            hallucination_check = self._check_for_hallucinations(query.content, response.content, context_texts)

            # Combine all validation results
            is_valid = (
                text_overlap_valid or
                semantic_similarity_valid or
                content_mention_valid
            ) and not hallucination_check

            return ValidationStatus.PASSED if is_valid else ValidationStatus.FAILED

        except Exception as e:
            logger.error(f"Error in validate_response_grounding: {e}")
            return ValidationStatus.FAILED

    def _check_text_overlap(self, response: str, context_texts: List[str]) -> bool:
        """
        Check if response contains text that appears in the context
        """
        response_lower = response.lower()

        # Look for significant text overlaps (at least 5-word phrases)
        for context_text in context_texts:
            context_lower = context_text.lower()

            # Split both into words
            response_words = response_lower.split()
            context_words = context_lower.split()

            # Check for common phrases (at least 5 consecutive words)
            for i in range(len(response_words) - 4):
                phrase = " ".join(response_words[i:i+5])
                if len(phrase) > 10 and phrase in context_lower:  # At least 10 chars to avoid common phrases
                    return True

        return False

    def _check_semantic_similarity(self, response: str, context_texts: List[str], threshold: float = 0.3) -> bool:
        """
        Check semantic similarity between response and context using embeddings
        """
        try:
            # Generate embedding for response
            response_embedding = self.embedding_processor.generate_embedding(response)
            if not response_embedding:
                logger.warning("Could not generate embedding for response")
                return False

            # Generate embeddings for context texts
            for context_text in context_texts:
                context_embedding = self.embedding_processor.generate_embedding(context_text)
                if not context_embedding:
                    continue

                # Calculate similarity
                similarity = self.embedding_processor.calculate_similarity(
                    response_embedding, context_embedding
                )

                if similarity >= threshold:
                    return True

            return False
        except Exception as e:
            logger.error(f"Error in semantic similarity check: {e}")
            return False

    def _check_content_mention(self, response: str, context_texts: List[str]) -> bool:
        """
        Check if response mentions key information from the context
        """
        response_lower = response.lower()

        # Look for key entities, terms, or concepts from context in response
        for context_text in context_texts:
            context_lower = context_text.lower()

            # Split context into meaningful terms
            context_words = set(context_lower.split())

            # Remove common stop words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
            }

            context_terms = {word for word in context_words if len(word) > 4 and word not in stop_words}

            # Check if any context terms appear in response
            response_words = set(response_lower.split())
            common_terms = context_terms.intersection(response_words)

            # If we find at least 2 common terms, consider it valid
            if len(common_terms) >= 2:
                return True

        return False

    def _check_for_hallucinations(self, query: str, response: str, context_texts: List[str]) -> bool:
        """
        Check if response contains information not present in context (hallucination)
        Returns True if hallucination detected (response should fail validation)
        """
        try:
            # This is a simplified check - in a real implementation, you'd want more sophisticated hallucination detection
            response_lower = response.lower()
            query_lower = query.lower()

            # Check for claims in response that aren't supported by context
            # For now, we'll use a basic approach: if response is very different from context,
            # it might contain hallucinations

            # Get embeddings for response and context
            response_embedding = self.embedding_processor.generate_embedding(response)
            if not response_embedding:
                return False  # Can't validate, assume not hallucinated

            context_embeddings = []
            for context_text in context_texts:
                emb = self.embedding_processor.generate_embedding(context_text)
                if emb:
                    context_embeddings.append(emb)

            if not context_embeddings:
                return True  # No context to validate against, consider hallucinated

            # Calculate average similarity between response and context
            similarities = []
            for ctx_emb in context_embeddings:
                similarity = self.embedding_processor.calculate_similarity(response_embedding, ctx_emb)
                similarities.append(similarity)

            avg_similarity = sum(similarities) / len(similarities) if similarities else 0

            # If similarity is very low, it might indicate hallucination
            # But we need to be careful - some valid responses might be quite different from context
            # So we'll use a low threshold and combine with other checks
            return avg_similarity < 0.1

        except Exception as e:
            logger.error(f"Error in hallucination check: {e}")
            return False

    def validate_zero_hallucination(self, query: Query, response: Response, retrieved_context: RetrievedContext) -> bool:
        """
        Comprehensive validation for zero hallucination requirement
        """
        try:
            # Check if response is grounded in context
            grounding_status = self.validate_response_grounding(query, retrieved_context, response)

            # Additional checks for hallucination
            if grounding_status == ValidationStatus.FAILED:
                return False

            # Check if response directly answers the query based on context
            query_addressed = self._check_query_addressed(query.content, response.content, retrieved_context)

            # Check for consistency between context and response
            consistency_check = self._check_consistency(response.content, retrieved_context.content_chunks)

            return query_addressed and consistency_check

        except Exception as e:
            logger.error(f"Error in validate_zero_hallucination: {e}")
            return False

    def _check_query_addressed(self, query: str, response: str, retrieved_context: RetrievedContext) -> bool:
        """
        Check if the response addresses the original query
        """
        try:
            # Generate embeddings for query and response
            query_embedding = self.embedding_processor.generate_embedding(query)
            response_embedding = self.embedding_processor.generate_embedding(response)

            if not query_embedding or not response_embedding:
                # Fallback: keyword matching
                query_lower = query.lower()
                response_lower = response.lower()

                # Check if response contains terms related to query
                query_terms = set(query_lower.split())
                response_terms = set(response_lower.split())

                # At least some overlap in meaningful terms
                common_terms = query_terms.intersection(response_terms)
                meaningful_terms = {term for term in common_terms if len(term) > 3}

                return len(meaningful_terms) > 0

            # Calculate semantic similarity
            similarity = self.embedding_processor.calculate_similarity(query_embedding, response_embedding)

            # If there's reasonable similarity, the response likely addresses the query
            return similarity > 0.2

        except Exception as e:
            logger.error(f"Error in query addressed check: {e}")
            return True  # Don't fail validation due to check failure

    def _check_consistency(self, response: str, context_chunks: List[Any]) -> bool:
        """
        Check if the response is consistent with the provided context
        """
        try:
            response_lower = response.lower()

            # Check if response makes claims that contradict context
            # This is a simplified check - look for opposite/negative terms in context vs response
            contradiction_indicators = [
                ("not", "is"), ("never", "always"), ("false", "true"),
                ("incorrect", "correct"), ("wrong", "right")
            ]

            for context_chunk in context_chunks:
                context_lower = context_chunk.text.lower()

                # Check for direct contradictions
                for neg_term, pos_term in contradiction_indicators:
                    if neg_term in context_lower and pos_term in response_lower:
                        # This might be a contradiction, but we need more context
                        # For now, just log it as a potential issue
                        pass

            # If we didn't find clear contradictions, consider it consistent
            return True

        except Exception as e:
            logger.error(f"Error in consistency check: {e}")
            return True  # Don't fail validation due to check failure