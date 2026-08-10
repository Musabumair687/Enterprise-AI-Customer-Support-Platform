"""Conversation history data-access operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Conversation


def list_conversations(db: Session, skip: int, limit: int) -> list[Conversation]:
    return list(db.scalars(select(Conversation).order_by(Conversation.created_at.desc()).offset(skip).limit(limit)))


def list_customer_conversations(db: Session, customer_id: int, limit: int) -> list[Conversation]:
    """Return the newest conversations for one CRM profile."""
    statement = select(Conversation).where(Conversation.customer_id == customer_id).order_by(Conversation.created_at.desc()).limit(limit)
    return list(db.scalars(statement))
