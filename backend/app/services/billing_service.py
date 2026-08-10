"""Billing data-access operations."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.models import Billing


def list_billing_records(db: Session, skip: int, limit: int) -> list[Billing]:
    return list(db.scalars(select(Billing).order_by(Billing.id).offset(skip).limit(limit)))


def get_billing_record(db: Session, invoice_id: int) -> Billing | None:
    return db.get(Billing, invoice_id)


def get_billing_by_invoice_number(db: Session, invoice_number: str) -> Billing | None:
    return db.scalar(select(Billing).where(Billing.invoice_number == invoice_number))


def search_billing_records(db: Session, customer_id: int | None, query: str | None, limit: int) -> list[Billing]:
    """Search customer billing records by invoice number or plan."""
    statement = select(Billing)
    if customer_id is not None:
        statement = statement.where(Billing.customer_id == customer_id)
    if query is not None:
        pattern = f"%{query.strip()}%"
        statement = statement.where(or_(Billing.invoice_number.ilike(pattern), Billing.plan.ilike(pattern)))
    return list(db.scalars(statement.order_by(Billing.created_at.desc()).limit(limit)))
