"""Technical-support troubleshooting agent."""
from app.agents.base import SpecializedAgent
class TechnicalAgent(SpecializedAgent):
    name = "technical_agent"
    allowed_tools = frozenset({"knowledge_base_search", "search_known_issues", "get_ticket", "search_tickets"})
    system_prompt = "You are Corvex technical support. Diagnose issues only from available evidence; do not invent error codes or fixes. Ask for relevant error messages when necessary."
