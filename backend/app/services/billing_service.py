"""Billing data-access operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Billing


def list_billing_records(db: Session, skip: int, limit: int) -> list[Billing]:
    return list(db.scalars(select(Billing).order_by(Billing.id).offset(skip).limit(limit)))


def get_billing_record(db: Session, invoice_id: int) -> Billing | None:
    return db.get(Billing, invoice_id)
