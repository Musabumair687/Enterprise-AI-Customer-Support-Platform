"""Ticket business operations and relationship validation."""

from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import Customer, Employee, Product, Ticket


def list_tickets(db: Session, skip: int, limit: int) -> list[Ticket]:
    return list(db.scalars(select(Ticket).order_by(Ticket.id).offset(skip).limit(limit)))


def get_ticket(db: Session, ticket_id: int) -> Ticket | None:
    return db.get(Ticket, ticket_id)


def search_tickets(db: Session, query: str, customer_id: int | None, limit: int) -> list[Ticket]:
    """Search case titles/descriptions, optionally within one customer's tickets."""
    pattern = f"%{query.strip()}%"
    statement = select(Ticket).where(or_(Ticket.title.ilike(pattern), Ticket.description.ilike(pattern)))
    if customer_id is not None:
        statement = statement.where(Ticket.customer_id == customer_id)
    return list(db.scalars(statement.order_by(Ticket.updated_at.desc()).limit(limit)))


def _validate_relations(db: Session, values: dict[str, Any]) -> str | None:
    relations = (
        ("customer_id", Customer, "Customer"),
        ("assigned_employee_id", Employee, "Employee"),
        ("product_id", Product, "Product"),
    )
    for field, model, label in relations:
        if field in values and values[field] is not None and db.get(model, values[field]) is None:
            return f"{label} {values[field]} was not found."
    return None


def create_ticket(db: Session, values: dict[str, Any]) -> tuple[Ticket | None, str | None]:
    relation_error = _validate_relations(db, values)
    if relation_error:
        return None, relation_error
    ticket = Ticket(**values)
    db.add(ticket)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None, "A ticket with this external ID already exists."
    db.refresh(ticket)
    return ticket, None


def update_ticket(db: Session, ticket: Ticket, values: dict[str, Any]) -> tuple[Ticket | None, str | None]:
    relation_error = _validate_relations(db, values)
    if relation_error:
        return None, relation_error
    for field, value in values.items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket, None


def delete_ticket(db: Session, ticket: Ticket) -> None:
    db.delete(ticket)
    db.commit()
