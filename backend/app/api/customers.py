"""Customer REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import CustomerRead
from app.schemas.response import APIResponse
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/search", response_model=APIResponse[list[CustomerRead]])
def search_customers(query: str = Query(min_length=1), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[CustomerRead]]:
    customers = customer_service.search_customers(db, query, skip, limit)
    return APIResponse(success=True, message="Customer search completed.", data=[CustomerRead.model_validate(customer) for customer in customers])


@router.get("", response_model=APIResponse[list[CustomerRead]])
def list_customers(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[CustomerRead]]:
    customers = customer_service.list_customers(db, skip, limit)
    return APIResponse(success=True, message="Customers retrieved successfully.", data=[CustomerRead.model_validate(customer) for customer in customers])


@router.get("/{customer_id}", response_model=APIResponse[CustomerRead])
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> APIResponse[CustomerRead]:
    customer = customer_service.get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found.")
    return APIResponse(success=True, message="Customer retrieved successfully.", data=CustomerRead.model_validate(customer))
