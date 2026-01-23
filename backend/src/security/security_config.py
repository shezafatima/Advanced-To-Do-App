"""
Security configuration for the Todo Full-Stack Web Application.

This module provides security hardening configurations and utilities.
"""

from typing import List, Optional
from datetime import timedelta

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import secrets

from ..logging.logger_config import get_logger


# Initialize security logger
security_logger = get_logger("security")


class SecurityConfig:
    """Security configuration class with all security-related settings."""

    def __init__(self):
        # JWT Configuration
        self.JWT_SECRET_KEY = self._get_secret_key()
        self.JWT_ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7

        # Rate Limiting Configuration
        self.RATE_LIMIT_DEFAULT = "100/minute"
        self.RATE_LIMIT_LOGIN = "5/minute"
        self.RATE_LIMIT_REGISTER = "3/hour"

        # Password Requirements
        self.MIN_PASSWORD_LENGTH = 8
        self.PASSWORD_REQUIRE_UPPERCASE = True
        self.PASSWORD_REQUIRE_LOWERCASE = True
        self.PASSWORD_REQUIRE_DIGITS = True
        self.PASSWORD_REQUIRE_SPECIAL_CHARS = True

        # CORS Configuration
        self.ALLOWED_ORIGINS = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
        ]
        self.ALLOW_CREDENTIALS = True
        self.ALLOW_METHODS = ["*"]
        self.ALLOW_HEADERS = ["*"]

        # Security Headers
        self.SECURE_COOKIES = False  # Set to True in production
        self.HSTS_ENABLED = True
        self.HSTS_MAX_AGE = 31536000  # 1 year
        self.HSTS_INCLUDE_SUBDOMAINS = True
        self.HSTS_PRELOAD = True
        self.X_CONTENT_TYPE_OPTIONS = "nosniff"
        self.X_FRAME_OPTIONS = "DENY"
        self.X_XSS_PROTECTION = "1; mode=block"

    def _get_secret_key(self) -> str:
        """Generate or retrieve JWT secret key."""
        # In production, this should come from environment variables
        # For development, we generate a random key
        import os
        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key or secret_key == "your-secret-key-here-32-characters-at-least":
            secret_key = secrets.token_urlsafe(32)
            security_logger.warning("Using generated secret key. Set JWT_SECRET_KEY environment variable for production.")
        return secret_key

    def validate_password(self, password: str) -> List[str]:
        """Validate password against security requirements."""
        errors = []

        if len(password) < self.MIN_PASSWORD_LENGTH:
            errors.append(f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long")

        if self.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        if self.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")

        if self.PASSWORD_REQUIRE_DIGITS and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")

        if self.PASSWORD_REQUIRE_SPECIAL_CHARS and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")

        return errors

    def get_password_hash(self, password: str) -> str:
        """Hash a password using bcrypt."""
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash."""
        import bcrypt
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Create global security configuration instance
security_config = SecurityConfig()


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def setup_security_headers(app: FastAPI):
    """Add security headers to the FastAPI application."""
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import Response

    class SecurityHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response: Response = await call_next(request)

            # Add security headers
            if security_config.HSTS_ENABLED:
                response.headers["Strict-Transport-Security"] = (
                    f"max-age={security_config.HSTS_MAX_AGE}; "
                    f"includeSubDomains; "
                    f"preload"
                )

            response.headers["X-Content-Type-Options"] = security_config.X_CONTENT_TYPE_OPTIONS
            response.headers["X-Frame-Options"] = security_config.X_FRAME_OPTIONS
            response.headers["X-XSS-Protection"] = security_config.X_XSS_PROTECTION
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

            return response

    app.add_middleware(SecurityHeadersMiddleware)


def setup_rate_limiting(app: FastAPI):
    """Add rate limiting to the FastAPI application."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def setup_security(app: FastAPI):
    """Apply all security configurations to the FastAPI application."""
    # Setup rate limiting
    setup_rate_limiting(app)

    # Setup security headers
    setup_security_headers(app)

    security_logger.info("Security configurations applied to the application")


def log_security_event(event_type: str, details: dict, user_id: Optional[str] = None):
    """Log security-related events."""
    security_logger.warning(f"SECURITY EVENT: {event_type} - Details: {details} - User: {user_id}")


def check_brute_force_attempts(user_email: str, request_ip: str) -> bool:
    """Check if there are too many failed attempts for a user or IP."""
    # This is a simplified version - in a real application, you'd track attempts in a database/cache
    # For now, we'll just log the attempt
    log_security_event(
        "login_attempt",
        {"email": user_email, "ip": request_ip},
        user_email
    )
    return True  # Allow the attempt for now


def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove potentially dangerous characters
    # This is a basic implementation - consider using a library like bleach for HTML sanitization
    if input_str is None:
        return None

    # Remove null bytes
    sanitized = input_str.replace('\x00', '')

    # Additional sanitization can be added here based on specific requirements
    return sanitized


def validate_jwt_token(token: str) -> Optional[dict]:
    """Validate a JWT token and return the payload if valid."""
    from jose import JWTError, jwt
    import datetime

    try:
        payload = jwt.decode(
            token,
            security_config.JWT_SECRET_KEY,
            algorithms=[security_config.JWT_ALGORITHM]
        )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.datetime.fromtimestamp(exp) < datetime.datetime.utcnow():
            return None

        return payload
    except JWTError:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token."""
    from jose import jwt
    import datetime

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})

    encoded_jwt = jwt.encode(
        to_encode,
        security_config.JWT_SECRET_KEY,
        algorithm=security_config.JWT_ALGORITHM
    )

    return encoded_jwt