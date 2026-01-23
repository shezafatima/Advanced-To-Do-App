"""
Logging configuration for the Todo Full-Stack Web Application.

This module provides centralized logging configuration for different environments
with appropriate log levels, formatters, and handlers.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    max_log_file_size: int = 10 * 1024 * 1024  # 10MB
    log_retention_days: int = 30


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        log_format: Format string for log messages

    Returns:
        Root logger configured with the specified settings
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler for all environments
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler for non-development environments if specified
    if log_file:
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Use RotatingFileHandler to manage log file size
        try:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
        except ImportError:
            # Fallback to basic file handler if RotatingFileHandler not available
            file_handler = logging.FileHandler(log_file_path)

        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Prevent propagation to avoid duplicate logs
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.propagate = False

    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.propagate = False

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Name of the logger (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_api_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[str] = None,
):
    """
    Log API request details for monitoring and debugging.

    Args:
        logger: Logger instance to use
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user ID for authenticated requests
    """
    user_info = f" (user: {user_id})" if user_id else ""
    logger.info(
        f"API REQUEST: {method} {path} -> {status_code} ({duration_ms:.2f}ms){user_info}"
    )


def log_security_event(
    logger: logging.Logger, event_type: str, details: dict, user_id: Optional[str] = None
):
    """
    Log security-related events.

    Args:
        logger: Logger instance to use
        event_type: Type of security event (login_attempt, auth_failure, etc.)
        details: Dictionary with event details
        user_id: Optional user ID associated with the event
    """
    user_info = f" (user: {user_id})" if user_id else ""
    logger.warning(f"SECURITY EVENT: {event_type}{user_info} - Details: {details}")


def log_error_trace(
    logger: logging.Logger, error: Exception, context: str = "", user_id: Optional[str] = None
):
    """
    Log detailed error information including traceback.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        context: Context information about where the error occurred
        user_id: Optional user ID associated with the error
    """
    user_info = f" (user: {user_id})" if user_id else ""
    logger.exception(
        f"ERROR TRACE: {type(error).__name__}: {str(error)} in {context}{user_info}"
    )


# Pre-configured loggers for different purposes
app_logger = logging.getLogger("app")
auth_logger = logging.getLogger("auth")
db_logger = logging.getLogger("database")
api_logger = logging.getLogger("api")


def configure_app_logging():
    """
    Configure logging for the entire application based on environment settings.
    """
    import os

    # Get environment-specific settings
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        log_level = os.getenv("LOG_LEVEL", "WARNING")
        log_file = os.getenv("LOG_FILE", "logs/prod.log")
    elif env == "staging":
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", "logs/staging.log")
    else:  # development
        log_level = os.getenv("LOG_LEVEL", "DEBUG")
        log_file = os.getenv("LOG_FILE")  # Often None in development

    setup_logging(
        log_level=log_level,
        log_file=log_file,
        log_format=os.getenv(
            "LOG_FORMAT",
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        ),
    )