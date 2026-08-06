"""
===============================================================================
Standard API Response Schema

Purpose:
--------
Every endpoint in this backend should return the same top-level response shape.
Keeping this contract consistent means the frontend does not need different
parsing logic for customers, tickets, billing, or future AI features.

Response format:
----------------
{
    "success": true,
    "message": "A clear description of the result.",
    "data": {}
}

Usage:
------
Use APIResponse for successful endpoints. Use build_error_response in global
exception handlers so failures use the same structure with success set to false.
===============================================================================
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    """A consistent response envelope for all backend API endpoints."""

    success: bool
    message: str
    data: DataT | None = None


def build_error_response(message: str, data: Any = None) -> dict[str, Any]:
    """Create the standard response body used for API errors."""
    return APIResponse[Any](success=False, message=message, data=data).model_dump()
