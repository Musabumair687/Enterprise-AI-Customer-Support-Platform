"""Application-facing entry point for executing the Phase 9 intent graph."""

from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage

from app.graph.builder import build_graph
from app.nodes.intent_classifier import IntentClassifierNode
from app.state.chat_state import ChatState


class CustomerSupportWorkflow:
    """Run a conversation through classification, routing, and a scoped agent."""

    def __init__(self, intent_classifier: IntentClassifierNode | None = None, agents: dict[str, object] | None = None) -> None:
        self.graph = build_graph(intent_classifier, agents)

    def invoke(self, message: str, session_id: str | None = None) -> ChatState:
        """Handle one customer message through its designated specialized agent."""
        return self.graph.invoke(self._initial_state([HumanMessage(content=message)], session_id or str(uuid4())))

    def invoke_messages(self, messages: list[BaseMessage], session_id: str) -> ChatState:
        """Classify a conversation from its latest non-empty human message."""
        return self.graph.invoke(self._initial_state(messages, session_id))

    @staticmethod
    def _initial_state(messages: list[BaseMessage], session_id: str) -> ChatState:
        return {"messages": messages, "session_id": session_id, "customer_id": None,
                "intent": None, "agent": None, "tool_calls": [], "retrieved_context": None,
                "tool_results": {}, "response": None, "metadata": {}}
