"""State passed through the Phase 9 intent-classification graph."""

from typing import TypedDict

from langchain_core.messages import BaseMessage

from app.schemas.intent import Intent


class ChatState(TypedDict):
    """Conversation data, its classified intent, and traceable classification metadata."""

    messages: list[BaseMessage]
    session_id: str
    intent: Intent | None
    metadata: dict[str, str | float | int | None]
