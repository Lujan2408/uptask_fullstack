import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.config import settings
import colorama

logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    if not settings.ENABLE_REQUEST_LOGGING:
      return await call_next(request)
    
    # Start timer
    start_time = time.time()

    # Log of request
    logger.info(
      f"Request Started: {colorama.Fore.YELLOW}{request.method} {request.url.path} {colorama.Style.RESET_ALL}",
      extra={
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
      }
    )

    # Process the request
    response = await call_next(request)

    # Calculate response time
    response_time = (time.time() - start_time) * 1000

    # Log of response
    logger.info(
      f"Request Completed: {colorama.Fore.YELLOW}{request.method} {request.url.path} {colorama.Style.RESET_ALL} - {colorama.Fore.GREEN}{response.status_code} {colorama.Style.RESET_ALL} in {colorama.Fore.YELLOW}{response_time:.2f}ms {colorama.Style.RESET_ALL}",
      extra={
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "response_time": response_time,
        "content_length": response.headers.get("content-length")
      }
    )

    return response 