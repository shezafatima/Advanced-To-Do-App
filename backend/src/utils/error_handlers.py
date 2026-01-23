"""
Error handling utilities for the Todo Full-Stack Web Application.

This module provides custom exceptions, error handlers, and response formatting
for consistent error handling throughout the application.
"""

from enum import Enum
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..logging.logger_config import get_logger


class ErrorCode(str, Enum):
    """Enumeration of application-specific error codes."""

    # Authentication errors
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"

    # User errors
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_USER_DATA = "INVALID_USER_DATA"

    # Todo errors
    TODO_NOT_FOUND = "TODO_NOT_FOUND"
    TODO_OWNER_MISMATCH = "TODO_OWNER_MISMATCH"
    INVALID_TODO_DATA = "INVALID_TODO_DATA"

    # Database errors
    DATABASE_CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR"
    DATABASE_INTEGRITY_ERROR = "DATABASE_INTEGRITY_ERROR"

    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"

    # System errors
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


class ErrorResponse(BaseModel):
    """Standard error response model."""

    detail: str
    error_code: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None


class AppException(HTTPException):
    """Custom application exception with extended error details."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: ErrorCode = None,
        headers: dict = None,
        request_id: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code.value if error_code else None
        self.request_id = request_id


class ValidationError(AppException):
    """Exception raised for validation errors."""

    def __init__(self, detail: str, request_id: str = None):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code=ErrorCode.VALIDATION_ERROR,
            request_id=request_id,
        )


class AuthenticationError(AppException):
    """Exception raised for authentication errors."""

    def __init__(self, detail: str = "Authentication failed", request_id: str = None):
        super().__init__(
            status_code=401,
            detail=detail,
            error_code=ErrorCode.AUTHENTICATION_FAILED,
            request_id=request_id,
        )


class AuthorizationError(AppException):
    """Exception raised for authorization errors."""

    def __init__(self, detail: str = "Insufficient permissions", request_id: str = None):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code=ErrorCode.INSUFFICIENT_PERMISSIONS,
            request_id=request_id,
        )


class ResourceNotFoundError(AppException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str, resource_id: str, request_id: str = None):
        detail = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(
            status_code=404,
            detail=detail,
            error_code=ErrorCode[f"{resource_type.upper()}_NOT_FOUND"],
            request_id=request_id,
        )


class DuplicateResourceError(AppException):
    """Exception raised when attempting to create a duplicate resource."""

    def __init__(self, resource_type: str, field: str, value: str, request_id: str = None):
        detail = f"{resource_type} with {field} '{value}' already exists"
        super().__init__(
            status_code=409,
            detail=detail,
            error_code=ErrorCode[f"{resource_type.upper()}_ALREADY_EXISTS"],
            request_id=request_id,
        )


def format_error_response(
    detail: str,
    error_code: str = None,
    request_id: str = None,
    path: str = None,
) -> Dict[str, Any]:
    """
    Format error response with consistent structure.

    Args:
        detail: Error message
        error_code: Application-specific error code
        request_id: Request ID for tracking
        path: Request path

    Returns:
        Dictionary with formatted error response
    """
    from datetime import datetime

    return {
        "detail": detail,
        "error_code": error_code,
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": path,
    }


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions.

    Args:
        request: FastAPI request object
        exc: Exception that occurred

    Returns:
        JSONResponse with error details
    """
    logger = get_logger(__name__)

    # Extract request ID if available
    request_id = getattr(request.state, 'request_id', None) if hasattr(request.state, 'request_id') else None
    path = str(request.url)

    # Log the error with traceback
    from ..logging.logger_config import log_error_trace
    log_error_trace(logger, exc, f"Unhandled exception in {path}", None)

    # Format error response
    error_response = format_error_response(
        detail="An internal server error occurred",
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        request_id=request_id,
        path=path,
    )

    return JSONResponse(
        status_code=500,
        content=error_response,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for HTTP exceptions.

    Args:
        request: FastAPI request object
        exc: HTTPException that occurred

    Returns:
        JSONResponse with error details
    """
    logger = get_logger(__name__)

    # Extract request ID if available
    request_id = getattr(request.state, 'request_id', None) if hasattr(request.state, 'request_id') else None
    path = str(request.url)

    # Log the error
    if exc.status_code >= 500:
        # Log server errors
        log_error_trace(logger, exc, f"HTTP {exc.status_code} error in {path}", None)
    elif exc.status_code >= 400:
        # Log client errors
        logger.info(f"HTTP {exc.status_code} error in {path}: {exc.detail}")

    # Handle AppException specifically
    if isinstance(exc, AppException):
        error_response = format_error_response(
            detail=exc.detail,
            error_code=exc.error_code,
            request_id=request_id,
            path=path,
        )
    else:
        error_response = format_error_response(
            detail=exc.detail,
            error_code=None,
            request_id=request_id,
            path=path,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=exc.headers,
    )


def add_exception_handlers(app):
    """
    Add global exception handlers to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(AppException, http_exception_handler)


def handle_database_error(db_error: Exception, context: str = "") -> AppException:
    """
    Convert database errors to application-specific exceptions.

    Args:
        db_error: Database exception that occurred
        context: Context where the error occurred

    Returns:
        AppException with appropriate status code and error code
    """
    logger = get_logger(__name__)
    logger.error(f"Database error in {context}: {str(db_error)}")

    # Import here to avoid circular imports
    import sqlalchemy.exc as sa_exc

    if isinstance(db_error, sa_exc.IntegrityError):
        # Handle constraint violations
        if "users.email" in str(db_error) or "UNIQUE constraint failed" in str(db_error):
            return DuplicateResourceError("user", "email", "provided_email")
        return AppException(
            status_code=409,
            detail="Database integrity constraint violation",
            error_code=ErrorCode.DATABASE_INTEGRITY_ERROR,
        )
    elif isinstance(db_error, sa_exc.DBAPIError):
        return AppException(
            status_code=503,
            detail="Database service temporarily unavailable",
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
        )
    else:
        return AppException(
            status_code=500,
            detail=f"Database error occurred: {str(db_error)}",
            error_code=ErrorCode.DATABASE_CONNECTION_ERROR,
        )


def validate_input(data: Dict[str, Any], required_fields: list, field_validators: Dict[str, callable] = None) -> Dict[str, Any]:
    """
    Validate input data against required fields and custom validators.

    Args:
        data: Input data dictionary
        required_fields: List of required field names
        field_validators: Dictionary mapping field names to validation functions

    Returns:
        Validated data if successful

    Raises:
        ValidationError if validation fails
    """
    errors = []

    # Check required fields
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and data[field].strip() == ""):
            errors.append(f"Field '{field}' is required")

    # Run custom validators
    if field_validators:
        for field, validator in field_validators.items():
            if field in data:
                try:
                    validator(data[field])
                except ValueError as e:
                    errors.append(f"Field '{field}' validation failed: {str(e)}")

    if errors:
        raise ValidationError(detail="; ".join(errors))

    return data