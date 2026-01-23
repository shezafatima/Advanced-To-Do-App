import time
import logging
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host}:{request.client.port} "
            f"with headers: {dict(request.headers)}"
        )

        response = await call_next(request)

        # Calculate process time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"for {request.method} {request.url.path} "
            f"processed in {process_time:.4f}s"
        )

        return response