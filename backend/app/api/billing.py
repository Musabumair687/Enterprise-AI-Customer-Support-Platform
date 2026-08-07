"""Billing REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import BillingRead
from app.schemas.response import APIResponse
from app.services import billing_service

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("", response_model=APIResponse[list[BillingRead]])
def list_billing(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[BillingRead]]:
    records = billing_service.list_billing_records(db, skip, limit)
    return APIResponse(success=True, message="Billing records retrieved successfully.", data=[BillingRead.model_validate(record) for record in records])


@router.get("/{invoice_id}", response_model=APIResponse[BillingRead])
def get_billing(invoice_id: int, db: Session = Depends(get_db)) -> APIResponse[BillingRead]:
    record = billing_service.get_billing_record(db, invoice_id)
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Billing record not found.")
    return APIResponse(success=True, message="Billing record retrieved successfully.", data=BillingRead.model_validate(record))
