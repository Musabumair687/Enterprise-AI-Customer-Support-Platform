"""Conversation-memory overview: persists and retrieves the auditable messages belonging to one session."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import ConversationMessage


class ConversationMemory:
    """Database operations for raw session messages; summaries never replace these records."""

    def save_message(
        self, db: Session, conversation_id: int, role: str, content: str, metadata: dict | None = None, turn_id: str | None = None
    ) -> ConversationMessage:
        """Store one validated message and make it available to the current transaction."""
        if turn_id is not None:
            existing = db.scalar(select(ConversationMessage).where(
                ConversationMessage.conversation_id == conversation_id,
                ConversationMessage.turn_id == turn_id,
                ConversationMessage.role == role,
            ))
            if existing is not None:
                return existing
        message = ConversationMessage(
            conversation_id=conversation_id, role=role, content=content, message_metadata=metadata, turn_id=turn_id
        )
        db.add(message)
        db.flush()
        return message

    def get_messages(self, db: Session, conversation_id: int) -> list[ConversationMessage]:
        """Return complete chronological history for audit and summary generation."""
        statement = select(ConversationMessage).where(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.created_at, ConversationMessage.id)
        return list(db.scalars(statement))

    def get_recent_messages(self, db: Session, conversation_id: int, limit: int = 15) -> list[ConversationMessage]:
        """Return the most recent messages in chronological order for the LLM working context."""
        statement = select(ConversationMessage).where(
            ConversationMessage.conversation_id == conversation_id
        ).order_by(ConversationMessage.created_at.desc(), ConversationMessage.id.desc()).limit(limit)
        return list(reversed(list(db.scalars(statement))))
