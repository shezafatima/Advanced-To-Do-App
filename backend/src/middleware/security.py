from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import re


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware for enhanced validation and protection.
    """

    # Block common SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+table)",
        r"(?i)(delete\s+from)",
        r"(?i)(insert\s+into)",
        r"(?i)(update\s+set)",
        r"(?i)(exec\s*\()",
        r"(?i)(execute\s*\()",
        r"'(\s*(and|or)\s*.*\s*[=<>])",
    ]

    # Block common XSS patterns
    XSS_PATTERNS = [
        r"(?i)<script[^>]*>",
        r"(?i)</script>",
        r"(?i)<iframe[^>]*>",
        r"(?i)</iframe>",
        r"(?i)<object[^>]*>",
        r"(?i)</object>",
        r"(?i)<embed[^>]*>",
        r"(?i)</embed>",
    ]

    async def dispatch(self, request: Request, call_next):
        # For POST and PUT requests, validate body content
        if request.method in ["POST", "PUT", "PATCH"]:
            body_bytes = await request.body()
            body_str = body_bytes.decode("utf-8")

            # Check for SQL injection patterns
            for pattern in self.SQL_INJECTION_PATTERNS:
                if re.search(pattern, body_str):
                    return JSONResponse(
                        status_code=400,
                        content={"detail": "Request contains potential SQL injection"}
                    )

            # Check for XSS patterns
            for pattern in self.XSS_PATTERNS:
                if re.search(pattern, body_str):
                    return JSONResponse(
                        status_code=400,
                        content={"detail": "Request contains potential XSS attack"}
                    )

        # Add security headers to response
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response