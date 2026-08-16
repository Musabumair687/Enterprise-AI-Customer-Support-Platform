"""Validated public contracts for Phase 11 memory candidates and graph-ready memory context."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


MemoryType = Literal["preference", "product_usage", "support_history", "account_context"]
MessageRole = Literal["user", "assistant", "tool", "system"]


class MemoryCandidate(BaseModel):
    """A proposed durable fact; validation prevents unrestricted long-term-memory writes."""

    memory_type: MemoryType
    content: str = Field(min_length=3, max_length=1_000)
    importance: int = Field(default=3, ge=1, le=5)
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class MemoryMessage(BaseModel):
    """A safe representation of one stored session message."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: MessageRole
    content: str
    created_at: datetime


class MemoryContext(BaseModel):
    """Persistent context loaded before LangGraph processes the newest customer message."""

    conversation_id: int
    session_id: str
    summary: str | None = None
    recent_messages: list[MemoryMessage] = Field(default_factory=list)
    long_term_memories: list[MemoryCandidate] = Field(default_factory=list)
    session_memory: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
