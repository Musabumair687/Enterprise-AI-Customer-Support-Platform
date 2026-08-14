"""Resolve a classified intent to the specialized-agent graph node."""
from app.graph.routes import route_for_intent
from app.state.chat_state import ChatState


def route_intent(state: ChatState) -> dict[str, str | dict[str, str]]:
    """Record the selected agent before LangGraph follows its conditional edge."""
    agent = route_for_intent(state.get("intent"))
    return {"agent": agent, "metadata": {**state.get("metadata", {}), "routing_status": "success", "routed_agent": agent}}
