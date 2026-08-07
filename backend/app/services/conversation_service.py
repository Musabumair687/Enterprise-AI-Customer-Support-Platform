"""Conversation history data-access operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Conversation


def list_conversations(db: Session, skip: int, limit: int) -> list[Conversation]:
    return list(db.scalars(select(Conversation).order_by(Conversation.created_at.desc()).offset(skip).limit(limit)))
