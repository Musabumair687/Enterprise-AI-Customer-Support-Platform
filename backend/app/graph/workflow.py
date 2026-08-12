"""Application-facing entry point for executing the Phase 8 routing graph."""

from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage

from app.graph.builder import build_graph
from app.nodes.router import RouterNode
from app.state.chat_state import ChatState


class CustomerSupportWorkflow:
    """Run a conversation through the initial routing-only graph."""

    def __init__(self, router: RouterNode | None = None) -> None:
        self.graph = build_graph(router)

    def invoke(self, message: str, session_id: str | None = None) -> ChatState:
        """Route one customer message; Phase 8 intentionally does not generate an answer."""
        state: ChatState = {
            "messages": [HumanMessage(content=message)],
            "session_id": session_id or str(uuid4()),
            "route": "unknown",
        }
        return self.graph.invoke(state)

    def invoke_messages(self, messages: list[BaseMessage], session_id: str) -> ChatState:
        """Route an existing conversation using its latest non-empty human message."""
        return self.graph.invoke({"messages": messages, "session_id": session_id, "route": "unknown"})
