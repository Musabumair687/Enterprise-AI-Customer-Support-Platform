"""
===============================================================================
API Version 1 Router

Purpose:
--------
This router is the single entry point for all Version 1 API endpoints.
main.py registers it with the /api/v1 prefix, so every route added here begins
with /api/v1. For example, a future customers router will be available at
/api/v1/customers.

Why version routes:
-------------------
When Version 2 is needed, we can add /api/v2 without changing or breaking
existing frontend pages and integrations that use /api/v1.

Current endpoint:
-----------------
GET /api/v1 confirms that Version 1 of the API is available and demonstrates
the standard API response format.
===============================================================================
"""

from fastapi import APIRouter, status

from app.api import billing, chat, conversations, customers, employees, health, products, tickets
from app.schemas.response import APIResponse


router = APIRouter()
router.include_router(health.router)
router.include_router(customers.router)
router.include_router(tickets.router)
router.include_router(billing.router)
router.include_router(products.router)
router.include_router(employees.router)
router.include_router(conversations.router)
router.include_router(chat.router)


@router.get("", response_model=APIResponse[dict[str, str]], status_code=status.HTTP_200_OK)
async def api_v1_status() -> APIResponse[dict[str, str]]:
    """Confirm that the Version 1 API router is available."""
    return APIResponse(
        success=True,
        message="API Version 1 is available.",
        data={"version": "v1"},
    )
