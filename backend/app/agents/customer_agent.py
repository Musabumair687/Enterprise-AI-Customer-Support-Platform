"""Customer account-support agent."""
from app.agents.base import SpecializedAgent
class CustomerAgent(SpecializedAgent):
    name = "customer_agent"
    allowed_tools = frozenset({"customer_lookup", "customer_search"})
    system_prompt = "You are Corvex customer support. Help with account questions without inventing customer data; request authenticated account context when needed."
