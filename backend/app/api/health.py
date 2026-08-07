"""Health endpoint for API and dependency monitoring."""

from fastapi import APIRouter, status
from sqlalchemy import text

from app.config import get_settings
from app.database.database import engine
from app.schemas.response import APIResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=APIResponse[dict[str, str]], status_code=status.HTTP_200_OK)
def health_check() -> APIResponse[dict[str, str]]:
    """Confirm that the API, validated configuration, and database are available."""
    get_settings()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return APIResponse(success=True, message="Service is healthy.", data={"api": "healthy", "database": "healthy", "configuration": "healthy"})
