"""
Logging middleware for the Todo Full-Stack Web Application.

This module provides middleware to log API requests, responses, and performance metrics.
"""

import time
import uuid
from typing import Optional

from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..logging.logger_config import api_logger, log_api_request, log_security_event, log_error_trace


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log API requests, responses, and performance metrics.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate request ID for tracking
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Get user ID if available
        user_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else None

        # Log request start
        start_time = time.time()
        api_logger.info(
            f"REQUEST START: {request_id} - {request.method} {request.url.path}",
            extra={"request_id": request_id, "user_id": user_id}
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Log the completed request
            log_api_request(
                api_logger,
                request.method,
                request.url.path,
                response.status_code,
                duration,
                user_id
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            # Log security events for certain status codes
            if response.status_code >= 400:
                log_security_event(
                    api_logger,
                    "api_error",
                    {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": duration
                    },
                    user_id
                )

            return response

        except Exception as e:
            # Calculate duration even if there was an error
            duration = (time.time() - start_time) * 1000

            # Log the error
            log_error_trace(
                api_logger,
                e,
                f"Request processing failed: {request.method} {request.url.path}",
                user_id
            )

            # Log the completed request with error status
            log_api_request(
                api_logger,
                request.method,
                request.url.path,
                500,  # Internal server error
                duration,
                user_id
            )

            # Re-raise the exception to be handled by FastAPI
            raise


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware to monitor API performance and track slow requests.
    """

    def __init__(self, app, slow_request_threshold: float = 1000.0):  # 1 second threshold
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request.state.start_time = start_time

        response = await call_next(request)

        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Log slow requests
        if duration > self.slow_request_threshold:
            user_id = getattr(request.state, 'user_id', None) if hasattr(request.state, 'user_id') else None

            api_logger.warning(
                f"SLOW REQUEST: {request.method} {request.url.path} took {duration:.2f}ms",
                extra={
                    "request_duration_ms": duration,
                    "method": request.method,
                    "path": request.url.path,
                    "user_id": user_id
                }
            )

        return response


def add_logging_middleware(app):
    """
    Add logging middleware to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    # Add performance monitoring middleware
    app.add_middleware(
        PerformanceMonitoringMiddleware,
        slow_request_threshold=1000.0  # Log requests taking more than 1 second
    )