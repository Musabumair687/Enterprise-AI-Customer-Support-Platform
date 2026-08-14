"""Human-handoff and complaint escalation agent."""
from app.agents.base import SpecializedAgent
class EscalationAgent(SpecializedAgent):
    name = "escalation_agent"
    allowed_tools = frozenset({"find_employee", "find_employee_by_skill", "find_support_agent", "assign_ticket", "escalate_ticket"})
    system_prompt = "You are Corvex escalation support. Acknowledge the request, explain the human handoff path, and do not claim an assignment occurred unless confirmed by a tool."
