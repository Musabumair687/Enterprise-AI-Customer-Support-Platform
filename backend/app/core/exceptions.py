"""
===============================================================================
Global Exception Handlers Module

Purpose:
--------
This module defines custom exception handlers for the FastAPI application.

Instead of allowing FastAPI to return its default error responses,
this module creates a consistent JSON error format for every API error.

Main Responsibilities:
----------------------
1. Handle HTTP exceptions (404, 401, 403, etc.).
2. Handle request validation errors.
3. Handle unexpected server errors.
4. Log every error for debugging.
5. Hide sensitive internal information from clients.

Workflow:
---------

Client Request
      │
      ▼
Request Processing
      │
      ▼
     Error?
      │
      ├──────── HTTP Error (404,401...)
      │               │
      │               ▼
      │      http_exception_handler()
      │
      ├──────── Validation Error
      │               │
      │               ▼
      │   validation_exception_handler()
      │
      └──────── Unexpected Exception
                      │
                      ▼
       unhandled_exception_handler()
                      │
                      ▼
          Log Error + Return JSON

Benefits:
---------
✓ Consistent API responses
✓ Easier debugging
✓ Better client experience
✓ Secure error handling
✓ Production-ready exception management

===============================================================================
"""
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger
from app.schemas.response import build_error_response


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Return a consistent response for HTTP errors such as 404."""
    get_logger().warning(
        "HTTP error | method=%s path=%s status=%s",
        request.method,
        request.url.path,
        exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(str(exc.detail)),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return a consistent response when request data does not validate."""
    get_logger().warning(
        "Validation error | method=%s path=%s errors=%s",
        request.method,
        request.url.path,
        exc.error_count(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=build_error_response("Request validation failed.", {"details": exc.errors()}),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Log unexpected failures while keeping internal details private."""
    get_logger().exception(
        "Unhandled error | method=%s path=%s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error_response("An unexpected server error occurred."),
    )
