"""FastAPI application entry point."""

from fastapi import FastAPI

from app.config import validate_settings


app = FastAPI(
    title="Enterprise AI Customer Support Platform",
    version="0.1.0",
    description=(
        "Backend API for the Enterprise AI Customer Support Platform. "
        "This service will power customer-support workflows and AI capabilities."
    ),
)


@app.on_event("startup")
async def startup_event() -> None:
    """Run application initialization when the server starts."""
    validate_settings()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Run application cleanup when the server stops."""
    # Future cleanup tasks (closing connections, flushing logs, etc.) go here.
    pass
