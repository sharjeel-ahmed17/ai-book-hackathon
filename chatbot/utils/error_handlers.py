from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import traceback
from pydantic import ValidationError


logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_error",
                "message": str(exc.detail),
                "status_code": exc.status_code
            }
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation exceptions"""
    logger.error(f"Validation Error: {exc}")

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"General Exception: {exc}\n{traceback.format_exc()}")

    # In production, you might not want to expose the full error message
    error_message = "Internal server error" if not request.app.debug else str(exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": error_message
            }
        }
    )


def add_error_handlers(app):
    """Add error handlers to the FastAPI app"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


# Custom exception classes
class RAGException(Exception):
    """Base exception for RAG-related errors"""
    def __init__(self, message: str, error_code: str = "RAG_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ContentRetrievalError(RAGException):
    """Raised when content retrieval fails"""
    def __init__(self, message: str = "Failed to retrieve relevant content"):
        super().__init__(message, "CONTENT_RETRIEVAL_ERROR")


class EmbeddingGenerationError(RAGException):
    """Raised when embedding generation fails"""
    def __init__(self, message: str = "Failed to generate embeddings"):
        super().__init__(message, "EMBEDDING_GENERATION_ERROR")


class ResponseGenerationError(RAGException):
    """Raised when response generation fails"""
    def __init__(self, message: str = "Failed to generate response"):
        super().__init__(message, "RESPONSE_GENERATION_ERROR")


class HallucinationDetectedError(RAGException):
    """Raised when hallucination is detected in response"""
    def __init__(self, message: str = "Response contains hallucinated content"):
        super().__init__(message, "HALLUCINATION_DETECTED")


class ServiceUnavailableError(RAGException):
    """Raised when an external service is unavailable"""
    def __init__(self, service_name: str):
        message = f"External service {service_name} is unavailable"
        super().__init__(message, "SERVICE_UNAVAILABLE")