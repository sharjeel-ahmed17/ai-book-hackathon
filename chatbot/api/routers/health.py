from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
import logging
from chatbot.config.settings import settings


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the service is running and dependencies are accessible.
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": settings.app_name,
            "version": "1.0.0",
            "dependencies": {
                "qdrant": "pending",  # Would check actual connection
                "postgres": "pending",  # Would check actual connection
                "embedding_service": "pending"  # Would check actual service
            }
        }

        # In a real implementation, you would check actual connections to services
        # For now, we'll mark them as available if the settings exist
        if settings.qdrant_api_key and settings.qdrant_url:
            health_status["dependencies"]["qdrant"] = "available"
        else:
            health_status["dependencies"]["qdrant"] = "not configured"

        if settings.neon_database_url:
            health_status["dependencies"]["postgres"] = "available"
        else:
            health_status["dependencies"]["postgres"] = "not configured"

        if settings.cohere_api_key or settings.openai_api_key or settings.gemini_api_key:
            health_status["dependencies"]["embedding_service"] = "available"
        else:
            health_status["dependencies"]["embedding_service"] = "not configured"

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/ready", summary="Readiness Check")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint to verify the service is ready to accept requests.
    """
    # In a real implementation, you would check if all required services are ready
    return {"status": "ready"}


@router.get("/info", summary="Service Information")
async def service_info() -> Dict[str, Any]:
    """
    Get detailed information about the service.
    """
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "api_v1_prefix": settings.api_v1_prefix,
        "max_query_length": settings.max_query_length,
        "max_response_length": settings.max_response_length,
        "response_timeout_seconds": settings.response_timeout_seconds,
        "timestamp": datetime.now().isoformat()
    }