"""Application-facing entry point for executing the Phase 9 intent graph."""

from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage

from app.graph.builder import build_graph
from app.nodes.intent_classifier import IntentClassifierNode
from app.state.chat_state import ChatState


class CustomerSupportWorkflow:
    """Run a conversation through the initial intent-classification graph."""

    def __init__(self, intent_classifier: IntentClassifierNode | None = None) -> None:
        self.graph = build_graph(intent_classifier)

    def invoke(self, message: str, session_id: str | None = None) -> ChatState:
        """Classify one message; Phase 9 intentionally does not generate an answer."""
        return self.graph.invoke({"messages": [HumanMessage(content=message)], "session_id": session_id or str(uuid4()), "intent": None, "metadata": {}})

    def invoke_messages(self, messages: list[BaseMessage], session_id: str) -> ChatState:
        """Classify a conversation from its latest non-empty human message."""
        return self.graph.invoke({"messages": messages, "session_id": session_id, "intent": None, "metadata": {}})
