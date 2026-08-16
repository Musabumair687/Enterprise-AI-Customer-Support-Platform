"""Session-memory overview: creates, retrieves, updates, and closes the current support conversation session."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import ConversationSession


class SessionMemory:
    """Own session identity and compact working facts such as current intent, product, and issue."""

    def get_session(self, db: Session, session_id: str) -> ConversationSession | None:
        """Find a persistent session by the identifier supplied by the client or graph."""
        return db.scalar(select(ConversationSession).where(ConversationSession.session_id == session_id))

    def create_session(self, db: Session, customer_id: int, session_id: str) -> ConversationSession:
        """Create one active session per unique session identifier."""
        session = ConversationSession(customer_id=customer_id, session_id=session_id, status="active", session_data={})
        db.add(session)
        db.flush()
        return session

    def get_or_create_session(self, db: Session, customer_id: int, session_id: str) -> ConversationSession:
        """Reuse a session only for its owning customer, preventing cross-customer context leakage."""
        session = self.get_session(db, session_id)
        if session is None:
            try:
                with db.begin_nested():
                    return self.create_session(db, customer_id, session_id)
            except IntegrityError:
                session = self.get_session(db, session_id)
                if session is None:
                    raise
        if session.customer_id != customer_id:
            raise ValueError("The supplied session does not belong to this customer.")
        return session

    def update_context(self, session: ConversationSession, **values: str | None) -> None:
        """Update only recognized compact session fields from graph state."""
        for name in ("current_intent", "current_product", "current_issue", "current_ticket"):
            if name in values and values[name] is not None:
                setattr(session, name, values[name])

    def close_session(self, session: ConversationSession) -> None:
        """Mark a completed session closed without deleting its audit trail."""
        session.status = "closed"
        session.ended_at = datetime.now(UTC)
