"""Construct the minimal START -> router -> END LangGraph workflow."""

from langgraph.graph import END, START, StateGraph

from app.nodes.router import RouterNode
from app.state.chat_state import ChatState


def build_graph(router: RouterNode | None = None):
    """Compile the Phase 8 routing graph without adding downstream branches yet."""
    graph = StateGraph(ChatState)
    graph.add_node("router", router or RouterNode())
    graph.add_edge(START, "router")
    graph.add_edge("router", END)
    return graph.compile()
