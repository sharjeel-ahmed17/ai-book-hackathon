import logging
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel
import json


class LogMetadata(BaseModel):
    """Structure for log metadata"""
    timestamp: str
    request_id: str
    user_id: str
    session_id: str
    endpoint: str
    method: str
    duration_ms: float
    status_code: int
    query: str = ""
    response_length: int = 0


class APILogger:
    """Utility class for API request/response logging"""

    def __init__(self, name: str = "rag_chatbot_api"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create a custom formatter
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_request(
        self,
        request_id: str,
        user_id: str,
        session_id: str,
        endpoint: str,
        method: str,
        query: str = ""
    ):
        """Log incoming request"""
        log_data = {
            "event": "request_received",
            "request_id": request_id,
            "user_id": user_id,
            "session_id": session_id,
            "endpoint": endpoint,
            "method": method,
            "query": query[:200] + "..." if len(query) > 200 else query,  # Truncate long queries
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_response(
        self,
        request_id: str,
        user_id: str,
        session_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: float,
        response_length: int = 0,
        query: str = ""
    ):
        """Log outgoing response"""
        log_data = {
            "event": "response_sent",
            "request_id": request_id,
            "user_id": user_id,
            "session_id": session_id,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "response_length": response_length,
            "query": query[:200] + "..." if len(query) > 200 else query,  # Truncate long queries
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data))

    def log_error(
        self,
        request_id: str,
        user_id: str,
        session_id: str,
        endpoint: str,
        method: str,
        error_message: str,
        error_type: str = "general"
    ):
        """Log error"""
        log_data = {
            "event": "error_occurred",
            "request_id": request_id,
            "user_id": user_id,
            "session_id": session_id,
            "endpoint": endpoint,
            "method": method,
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.error(json.dumps(log_data))

    def log_validation_result(
        self,
        request_id: str,
        session_id: str,
        validation_status: str,
        validation_details: str = ""
    ):
        """Log validation results"""
        log_data = {
            "event": "validation_result",
            "request_id": request_id,
            "session_id": session_id,
            "validation_status": validation_status,
            "validation_details": validation_details,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(json.dumps(log_data))