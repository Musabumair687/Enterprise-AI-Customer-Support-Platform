"""Construct the minimal START -> intent_classifier -> END LangGraph workflow."""

from langgraph.graph import END, START, StateGraph

from app.nodes.intent_classifier import IntentClassifierNode
from app.state.chat_state import ChatState


def build_graph(intent_classifier: IntentClassifierNode | None = None):
    """Compile the Phase 9 classification graph without downstream branches yet."""
    graph = StateGraph(ChatState)
    graph.add_node("intent_classifier", intent_classifier or IntentClassifierNode())
    graph.add_edge(START, "intent_classifier")
    graph.add_edge("intent_classifier", END)
    return graph.compile()
