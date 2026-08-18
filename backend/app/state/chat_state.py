"""State passed through the specialized-agent support graph."""

from typing import Any, TypedDict

from langchain_core.messages import BaseMessage

from app.schemas.intent import Intent


class ChatState(TypedDict, total=False):
    """Conversation data plus the trace needed to audit an agent response."""

    messages: list[BaseMessage]
    session_id: str
    turn_id: str
    customer_id: int | None
    conversation_id: int | None
    intent: Intent | None
    agent: str | None
    current_agent: str | None
    next_agent: str | None
    task: str | None
    subtasks: list[dict[str, object]]
    agent_results: dict[str, dict[str, object]]
    agent_step_count: int
    available_agents: list[str]
    confidence_score: float
    escalation_required: bool
    escalation_reason: str | None
    assigned_employee: dict[str, object] | None
    ticket_id: int | None
    tool_calls: list[str]
    retrieved_context: str | None
    tool_results: dict[str, Any]
    response: str | None
    conversation_summary: str | None
    recent_messages: list[dict[str, object]]
    long_term_memories: list[dict[str, object]]
    session_memory: dict[str, object]
    metadata: dict[str, Any]
