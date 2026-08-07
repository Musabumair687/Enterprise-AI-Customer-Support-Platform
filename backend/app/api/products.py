"""Product REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import ProductRead
from app.schemas.response import APIResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=APIResponse[list[ProductRead]])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[ProductRead]]:
    products = product_service.list_products(db, skip, limit)
    return APIResponse(success=True, message="Products retrieved successfully.", data=[ProductRead.model_validate(product) for product in products])


@router.get("/{product_id}", response_model=APIResponse[ProductRead])
def get_product(product_id: int, db: Session = Depends(get_db)) -> APIResponse[ProductRead]:
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found.")
    return APIResponse(success=True, message="Product retrieved successfully.", data=ProductRead.model_validate(product))
