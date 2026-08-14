"""State passed through the specialized-agent support graph."""

from typing import Any, TypedDict

from langchain_core.messages import BaseMessage

from app.schemas.intent import Intent


class ChatState(TypedDict, total=False):
    """Conversation data plus the trace needed to audit an agent response."""

    messages: list[BaseMessage]
    session_id: str
    customer_id: int | None
    intent: Intent | None
    agent: str | None
    tool_calls: list[str]
    retrieved_context: str | None
    tool_results: dict[str, Any]
    response: str | None
    metadata: dict[str, Any]
