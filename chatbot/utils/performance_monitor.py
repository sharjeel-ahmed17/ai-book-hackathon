import time
import asyncio
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
import threading
import logging


@dataclass
class PerformanceMetric:
    """Data class to store performance metrics"""
    request_id: str
    endpoint: str
    method: str
    start_time: float
    end_time: float
    duration_ms: float
    status_code: int
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    query_length: int = 0


class PerformanceMonitor:
    """Monitor API performance and response times"""

    def __init__(self, max_metrics: int = 1000):
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric"""
        with self.lock:
            self.metrics.append(metric)

    def get_average_response_time(self, endpoint: Optional[str] = None,
                                  time_window_minutes: int = 5) -> Optional[float]:
        """Get average response time for a specific endpoint or overall"""
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            relevant_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and
                (endpoint is None or m.endpoint == endpoint)
            ]

        if not relevant_metrics:
            return None

        total_duration = sum(m.duration_ms for m in relevant_metrics)
        return total_duration / len(relevant_metrics)

    def get_p95_response_time(self, endpoint: Optional[str] = None,
                              time_window_minutes: int = 5) -> Optional[float]:
        """Get 95th percentile response time"""
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            relevant_metrics = [
                m.duration_ms for m in self.metrics
                if m.end_time >= cutoff_time and
                (endpoint is None or m.endpoint == endpoint)
            ]

        if not relevant_metrics:
            return None

        # Calculate 95th percentile
        sorted_durations = sorted(relevant_metrics)
        index = int(0.95 * len(sorted_durations))
        return sorted_durations[index] if index < len(sorted_durations) else sorted_durations[-1]

    def get_request_count(self, endpoint: Optional[str] = None,
                         time_window_minutes: int = 5) -> int:
        """Get request count for a specific endpoint or overall"""
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            relevant_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and
                (endpoint is None or m.endpoint == endpoint)
            ]

        return len(relevant_metrics)

    def get_error_rate(self, endpoint: Optional[str] = None,
                       time_window_minutes: int = 5) -> float:
        """Get error rate as a percentage"""
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            relevant_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and
                (endpoint is None or m.endpoint == endpoint)
            ]

        if not relevant_metrics:
            return 0.0

        error_count = sum(1 for m in relevant_metrics if m.status_code >= 400)
        return (error_count / len(relevant_metrics)) * 100

    def is_performing_well(self, endpoint: Optional[str] = None,
                           max_avg_response_time: float = 2000.0,
                           max_p95_response_time: float = 5000.0,
                           max_error_rate: float = 5.0) -> bool:
        """Check if performance is within acceptable bounds"""
        avg_response = self.get_average_response_time(endpoint)
        p95_response = self.get_p95_response_time(endpoint)
        error_rate = self.get_error_rate(endpoint)

        # Check if any metric exceeds the threshold
        if avg_response and avg_response > max_avg_response_time:
            self.logger.warning(f"Average response time too high: {avg_response}ms")
            return False

        if p95_response and p95_response > max_p95_response_time:
            self.logger.warning(f"P95 response time too high: {p95_response}ms")
            return False

        if error_rate > max_error_rate:
            self.logger.warning(f"Error rate too high: {error_rate}%")
            return False

        return True

    def get_performance_summary(self, endpoint: Optional[str] = None,
                               time_window_minutes: int = 5) -> Dict[str, Any]:
        """Get a summary of performance metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "time_window_minutes": time_window_minutes,
            "endpoint": endpoint,
            "average_response_time_ms": self.get_average_response_time(endpoint, time_window_minutes),
            "p95_response_time_ms": self.get_p95_response_time(endpoint, time_window_minutes),
            "request_count": self.get_request_count(endpoint, time_window_minutes),
            "error_rate_percent": self.get_error_rate(endpoint, time_window_minutes),
            "is_performing_well": self.is_performing_well(endpoint)
        }


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def performance_monitor_middleware(app):
    """Middleware to monitor API performance"""
    async def monitor_middleware(request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, 'request_id', 'unknown')

        try:
            response = await call_next(request)
        finally:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            # Extract information from request
            endpoint = request.url.path
            method = request.method
            status_code = response.status_code

            # Get user and session info if available
            user_id = getattr(request.state, 'user_id', None)
            session_id = getattr(request.state, 'session_id', None)

            # Get query length if available (for query endpoints)
            query_length = 0
            if endpoint.endswith('/query') and request.method == 'POST':
                # This would require reading the request body, which is complex in middleware
                # For now, we'll skip this or implement differently
                pass

            # Record the metric
            metric = PerformanceMetric(
                request_id=request_id,
                endpoint=endpoint,
                method=method,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                status_code=status_code,
                user_id=user_id,
                session_id=session_id,
                query_length=query_length
            )

            perf_monitor.record_metric(metric)

            # Add performance header to response
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            # Log performance warning if response is too slow
            if duration_ms > 2000:  # More than 2 seconds
                perf_monitor.logger.warning(
                    f"Slow response detected: {endpoint} took {duration_ms:.2f}ms"
                )

        return response

    return monitor_middleware