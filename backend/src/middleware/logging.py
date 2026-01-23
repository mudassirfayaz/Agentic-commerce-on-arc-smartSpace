"""Logging middleware for FastAPI."""

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response."""
        start_time = time.time()
        
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "remote_addr": request.client.host if request.client else None
            }
        )
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} ({duration:.3f}s)",
            extra={
                "status_code": response.status_code,
                "duration": duration
            }
        )
        
        return response


def register_logging_middleware(app):
    """Register logging middleware."""
    app.add_middleware(LoggingMiddleware)
