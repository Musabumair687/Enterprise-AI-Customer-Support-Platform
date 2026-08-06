"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import router as api_v1_router
from app.config import validate_settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import configure_logging, get_logger, request_logging_middleware
from app.schemas.response import APIResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Validate settings and initialize shared resources during app lifecycle."""
    settings = validate_settings()
    logger = configure_logging(settings)
    logger.info("Application startup complete.")
    yield
    get_logger().info("Application shutdown complete.")


app = FastAPI(
    title="Enterprise AI Customer Support Platform",
    version="0.1.0",
    description=(
        "Backend API for the Enterprise AI Customer Support Platform. "
        "This service will power customer-support workflows and AI capabilities."
    ),
    lifespan=lifespan,
)

app.middleware("http")(request_logging_middleware)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.include_router(api_v1_router, prefix="/api/v1", tags=["API v1"])


@app.get("/", response_model=APIResponse[dict[str, str]], tags=["System"])
async def root() -> APIResponse[dict[str, str]]:
    """Return basic service information for a running backend instance."""
    return APIResponse(
        success=True,
        message="Enterprise AI Customer Support Platform backend is running.",
        data={"service": "enterprise-ai-customer-support-platform", "version": app.version},
    )


@app.get("/health", response_model=APIResponse[dict[str, str]], tags=["System"])
async def health_check() -> APIResponse[dict[str, str]]:
    """
    Check whether the backend process is running and ready to receive requests.

    This is intentionally a lightweight check for Phase 1. In later phases it
    will also verify dependencies such as the database, vector store, and cache.
    """
    return APIResponse(
        success=True,
        message="Service is healthy.",
        data={"status": "healthy"},
    )
