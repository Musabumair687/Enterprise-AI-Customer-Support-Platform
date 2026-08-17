"""Phase 12 bounded supervisor graph for sequential specialist collaboration."""
from langgraph.graph import END, START, StateGraph
from app.agents import BillingAgent, CustomerAgent, EscalationAgent, ProductAgent, SalesAgent, SupervisorAgent, TechnicalAgent
from app.graph.collaboration import record_agent_step, route_supervisor
from app.nodes.intent_classifier import IntentClassifierNode
from app.memory.memory_manager import MemoryManager
from app.state.chat_state import ChatState

def build_graph(intent_classifier: IntentClassifierNode | None = None, agents: dict[str, object] | None = None, memory_manager: MemoryManager | None = None, supervisor: SupervisorAgent | None = None):
    """Compile memory -> classifier -> supervisor <-> one worker -> memory save -> END."""
    configured = agents or {"customer_agent": CustomerAgent(), "billing_agent": BillingAgent(), "technical_agent": TechnicalAgent(), "product_agent": ProductAgent(), "escalation_agent": EscalationAgent(), "sales_agent": SalesAgent()}
    active_supervisor = supervisor or SupervisorAgent(available_agents=frozenset(configured))
    active_supervisor.set_available_agents(frozenset(configured))
    memory = memory_manager or MemoryManager()
    graph = StateGraph(ChatState)
    graph.add_node("load_memory", memory.load_graph_state)
    graph.add_node("intent_classifier", intent_classifier or IntentClassifierNode())
    graph.add_node("supervisor", active_supervisor)
    for name, agent in configured.items(): graph.add_node(name, agent)
    graph.add_node("record_agent_step", record_agent_step)
    graph.add_node("save_memory", memory.save_graph_state)
    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "intent_classifier")
    graph.add_edge("intent_classifier", "supervisor")
    graph.add_conditional_edges("supervisor", route_supervisor, {**{name: name for name in configured}, "save_memory": "save_memory"})
    for name in configured:
        graph.add_edge(name, "record_agent_step")
    graph.add_edge("record_agent_step", "supervisor")
    graph.add_edge("save_memory", END)
    return graph.compile()
