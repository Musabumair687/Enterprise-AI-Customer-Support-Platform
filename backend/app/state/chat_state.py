"""Minimal state passed through the Phase 8 customer-support graph."""

from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage


Route = Literal[
    "knowledge",
    "ticket",
    "billing",
    "technical_support",
    "account",
    "escalation",
    "unknown",
]


class ChatState(TypedDict):
    """Conversation data plus the single routing decision produced in Phase 8."""

    messages: list[BaseMessage]
    session_id: str
    route: Route
