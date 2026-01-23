import time
from collections import defaultdict, deque
from typing import Dict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_limit: int = 100, window_seconds: int = 3600):
        """
        Initialize the rate limiter.

        Args:
            app: The FastAPI app instance
            requests_limit: Number of requests allowed per window
            window_seconds: Time window in seconds (default: 1 hour = 3600 seconds)
        """
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, client_ip: str) -> bool:
        """
        Check if the client is allowed to make a request.
        """
        now = time.time()
        # Remove requests that are outside the time window
        while (self.requests[client_ip] and
               now - self.requests[client_ip][0] > self.window_seconds):
            self.requests[client_ip].popleft()

        # Check if the client has exceeded the limit
        if len(self.requests[client_ip]) >= self.requests_limit:
            return False

        # Add the current request
        self.requests[client_ip].append(now)
        return True

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host
        if not self.is_allowed(client_ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        response = await call_next(request)
        return response