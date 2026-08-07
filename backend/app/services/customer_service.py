"""Customer data-access and search operations."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.models import Customer


def list_customers(db: Session, skip: int, limit: int) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.id).offset(skip).limit(limit)))


def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def search_customers(db: Session, query: str, skip: int, limit: int) -> list[Customer]:
    pattern = f"%{query.strip()}%"
    statement = (
        select(Customer)
        .where(or_(Customer.name.ilike(pattern), Customer.email.ilike(pattern), Customer.company.ilike(pattern)))
        .order_by(Customer.name)
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement))
