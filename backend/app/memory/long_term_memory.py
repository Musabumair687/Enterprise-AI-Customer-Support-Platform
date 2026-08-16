"""Long-term-memory overview: validates and stores only durable, cross-session customer facts."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import CustomerMemory
from app.schemas.memory import MemoryCandidate


class LongTermMemory:
    """Persist approved memory candidates with deduplication; conversational filler never reaches this layer."""

    def save_memory(self, db: Session, customer_id: int, candidate: MemoryCandidate) -> CustomerMemory:
        """Insert or strengthen an identical approved fact instead of creating a duplicate."""
        normalized_content = candidate.content.strip().lower()
        statement = select(CustomerMemory).where(
            CustomerMemory.customer_id == customer_id,
            CustomerMemory.memory_type == candidate.memory_type,
            CustomerMemory.content_normalized == normalized_content,
        )
        memory = db.scalar(statement)
        if memory is None:
            memory = CustomerMemory(
                customer_id=customer_id,
                memory_type=candidate.memory_type,
                content=candidate.content.strip(),
                content_normalized=normalized_content,
                importance=candidate.importance,
                memory_metadata=candidate.metadata or None,
            )
            db.add(memory)
        else:
            memory.importance = max(memory.importance, candidate.importance)
            memory.memory_metadata = {**(memory.memory_metadata or {}), **candidate.metadata}
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            memory = db.scalar(statement)
            if memory is None:
                raise
        return memory

    def get_customer_memories(self, db: Session, customer_id: int) -> list[CustomerMemory]:
        """Load durable facts ordered by business importance and recency."""
        statement = select(CustomerMemory).where(CustomerMemory.customer_id == customer_id).order_by(
            CustomerMemory.importance.desc(), CustomerMemory.updated_at.desc()
        )
        return list(db.scalars(statement))
