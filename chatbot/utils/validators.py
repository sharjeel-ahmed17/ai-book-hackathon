from typing import Optional, Dict, Any, List
from pydantic import BaseModel, validator, ValidationError
import re


class QueryValidator:
    """Validation utilities for query inputs"""

    @staticmethod
    def validate_query_length(query: str, max_length: int = 1000) -> bool:
        """Validate that query length is within acceptable limits"""
        return 0 < len(query.strip()) <= max_length

    @staticmethod
    def validate_query_content(query: str) -> List[str]:
        """Validate query content and return list of validation errors"""
        errors = []

        if not query or not query.strip():
            errors.append("Query cannot be empty")

        if len(query.strip()) > 1000:  # Default max length
            errors.append("Query exceeds maximum length of 1000 characters")

        # Check for potentially harmful content (basic validation)
        harmful_patterns = [
            r'<script',  # Potential XSS
            r'javascript:',  # Potential XSS
            r'on\w+\s*=',  # Event handlers
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                errors.append(f"Query contains potentially harmful content: {pattern}")

        return errors

    @staticmethod
    def sanitize_query(query: str) -> str:
        """Basic sanitization of query input"""
        # Remove potentially harmful content (basic approach)
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', query, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        return sanitized.strip()


class ContentValidator:
    """Validation utilities for book content"""

    @staticmethod
    def validate_content_length(content: str, min_length: int = 10, max_length: int = 10000) -> bool:
        """Validate that content length is within acceptable limits"""
        content_stripped = content.strip()
        return min_length <= len(content_stripped) <= max_length

    @staticmethod
    def validate_content_type(content: str, allowed_types: List[str] = ["text", "markdown", "html"]) -> bool:
        """Validate content type"""
        # This is a simplified check - in real implementation you might want to detect content type
        return True

    @staticmethod
    def validate_source_reference(source_ref: str) -> List[str]:
        """Validate source reference format and return list of validation errors"""
        errors = []

        if not source_ref or not source_ref.strip():
            errors.append("Source reference cannot be empty")

        # Add more specific validation rules as needed
        # For example, check if it follows a specific format

        return errors


class ResponseValidator:
    """Validation utilities for responses"""

    @staticmethod
    def validate_response_content(response: str, max_length: int = 2000) -> List[str]:
        """Validate response content and return list of validation errors"""
        errors = []

        if not response or not response.strip():
            errors.append("Response cannot be empty")

        if len(response) > max_length:
            errors.append(f"Response exceeds maximum length of {max_length} characters")

        # Check for potentially harmful content
        harmful_patterns = [
            r'<script',  # Potential XSS
            r'javascript:',  # Potential XSS
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                errors.append(f"Response contains potentially harmful content: {pattern}")

        return errors

    @staticmethod
    def validate_source_attribution(source_references: List[Dict[str, Any]]) -> List[str]:
        """Validate source attribution and return list of validation errors"""
        errors = []

        if not source_references:
            errors.append("Response must include source references")

        for i, ref in enumerate(source_references):
            if not isinstance(ref, dict):
                errors.append(f"Source reference at index {i} must be a dictionary")
                continue

            if "reference" not in ref or not ref["reference"]:
                errors.append(f"Source reference at index {i} must include 'reference' field")

            if "text" not in ref or not ref["text"]:
                errors.append(f"Source reference at index {i} must include 'text' field")

        return errors


class SessionValidator:
    """Validation utilities for session management"""

    @staticmethod
    def validate_session_id(session_id: str) -> List[str]:
        """Validate session ID format and return list of validation errors"""
        errors = []

        if not session_id or not session_id.strip():
            errors.append("Session ID cannot be empty")

        # Basic UUID format check (simplified)
        uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        if session_id and not re.match(uuid_pattern, session_id):
            # If not in UUID format, it might be a custom session ID, which is acceptable
            pass  # Allow custom session IDs

        return errors


class GeneralValidator:
    """General validation utilities"""

    @staticmethod
    def validate_api_key(api_key: Optional[str]) -> bool:
        """Validate that API key is provided and not empty"""
        return bool(api_key and api_key.strip())

    @staticmethod
    def validate_url(url: str) -> bool:
        """Basic URL validation"""
        if not url:
            return False

        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None