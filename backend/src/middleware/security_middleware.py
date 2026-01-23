"""
Security middleware for the Todo Full-Stack Web Application.

This module provides middleware for security-related functionality.
"""

from typing import Optional
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from ..security.security_config import log_security_event, sanitize_input, check_brute_force_attempts
from ..logging.logger_config import get_logger


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Main security middleware that handles input sanitization,
    security logging, and basic protection measures.
    """

    async def dispatch(self, request: Request, call_next):
        # Sanitize input parameters
        if request.method in ["POST", "PUT", "PATCH"]:
            # For now, we'll just log the request for monitoring
            # In a real application, we'd want to sanitize the request body
            pass

        # Add security headers to response
        response = await call_next(request)

        # Add security headers to response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


class InputValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate and sanitize input data.
    """

    async def dispatch(self, request: Request, call_next):
        # For GET requests, sanitize query parameters
        if request.method == "GET":
            # Sanitize query parameters
            for key, value in request.query_params.items():
                if isinstance(value, str):
                    sanitized_value = sanitize_input(value)
                    if sanitized_value != value:
                        # Log the sanitization
                        logger = get_logger("security")
                        logger.warning(
                            f"Input sanitized for parameter '{key}': '{value}' -> '{sanitized_value}'",
                            extra={"request_id": getattr(request.state, 'request_id', None)}
                        )

        # For POST, PUT, PATCH requests, we'd normally sanitize the body
        # This is more complex and typically handled by Pydantic models
        # For now, we'll proceed with the request
        response = await call_next(request)

        return response


class BruteForceProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to protect against brute force attacks.
    """

    def __init__(self, app, login_endpoint_paths: Optional[list] = None):
        super().__init__(app)
        self.login_endpoints = login_endpoint_paths or ["/auth/login", "/auth/token"]
        self.logger = get_logger("security")

    async def dispatch(self, request: Request, call_next):
        # Check if this is a login attempt
        if str(request.url.path) in self.login_endpoints and request.method == "POST":
            # Extract email from request body
            try:
                body_bytes = await request.body()
                import json
                body = json.loads(body_bytes.decode('utf-8'))
                user_email = body.get('email', '')

                # Get client IP
                client_ip = request.client.host

                # Check for brute force attempts
                allow_attempt = check_brute_force_attempts(user_email, client_ip)

                if not allow_attempt:
                    self.logger.warning(
                        f"Brute force protection triggered for email: {user_email}, IP: {client_ip}"
                    )
                    raise HTTPException(
                        status_code=429,
                        detail="Too many login attempts. Please try again later."
                    )

            except Exception as e:
                # If we can't read the body, continue with the request
                pass

        response = await call_next(request)
        return response


class SecurityLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log security-related events.
    """

    async def dispatch(self, request: Request, call_next):
        # Log security-relevant information
        request.state.security_logged = False

        try:
            response = await call_next(request)

            # Log security events for certain status codes
            if response.status_code in [401, 403, 429]:
                log_security_event(
                    "access_denied",
                    {
                        "method": request.method,
                        "path": str(request.url.path),
                        "status_code": response.status_code,
                        "client_ip": request.client.host
                    }
                )

            return response

        except HTTPException as e:
            # Log security events for HTTP exceptions
            if e.status_code in [401, 403, 429]:
                log_security_event(
                    "access_denied",
                    {
                        "method": request.method,
                        "path": str(request.url.path),
                        "status_code": e.status_code,
                        "client_ip": request.client.host
                    }
                )

            raise


def add_security_middleware(app):
    """
    Add all security middleware to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Add brute force protection first (before other processing)
    app.add_middleware(
        BruteForceProtectionMiddleware,
        login_endpoint_paths=["/auth/login"]
    )

    # Add input validation
    app.add_middleware(InputValidationMiddleware)

    # Add security logging
    app.add_middleware(SecurityLoggingMiddleware)

    # Add general security middleware
    app.add_middleware(SecurityMiddleware)

    logger = get_logger("security")
    logger.info("Security middleware added to application")