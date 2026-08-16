"""Phase 10 conditional graph from intent classification to specialized agents."""
from langgraph.graph import END, START, StateGraph
from app.agents import BillingAgent, CustomerAgent, EscalationAgent, ProductAgent, SalesAgent, TechnicalAgent
from app.nodes.intent_classifier import IntentClassifierNode
from app.nodes.router import route_intent
from app.memory.memory_manager import MemoryManager
from app.state.chat_state import ChatState

def build_graph(intent_classifier: IntentClassifierNode | None = None, agents: dict[str, object] | None = None, memory_manager: MemoryManager | None = None):
    """Compile persistent memory load -> classifier -> specialized agent -> memory save -> END."""
    configured = agents or {"customer_agent": CustomerAgent(), "billing_agent": BillingAgent(), "technical_agent": TechnicalAgent(), "product_agent": ProductAgent(), "escalation_agent": EscalationAgent(), "sales_agent": SalesAgent()}
    memory = memory_manager or MemoryManager()
    graph = StateGraph(ChatState)
    graph.add_node("load_memory", memory.load_graph_state)
    graph.add_node("intent_classifier", intent_classifier or IntentClassifierNode())
    for name, agent in configured.items(): graph.add_node(name, agent)
    graph.add_node("router", route_intent)
    graph.add_node("save_memory", memory.save_graph_state)
    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "intent_classifier")
    graph.add_edge("intent_classifier", "router")
    graph.add_conditional_edges("router", lambda state: state["agent"], {name: name for name in configured})
    for name in configured: graph.add_edge(name, "save_memory")
    graph.add_edge("save_memory", END)
    return graph.compile()
