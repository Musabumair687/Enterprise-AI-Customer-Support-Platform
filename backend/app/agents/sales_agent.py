"""Sales and upgrade inquiry agent."""
from app.agents.base import SpecializedAgent
class SalesAgent(SpecializedAgent):
    name = "sales_agent"
    allowed_tools = frozenset({"get_product", "list_products", "get_customer_crm_profile", "customer_lookup", "knowledge_base_search"})
    system_prompt = "You are Corvex sales support. Help with purchasing and upgrades using verified product information; do not invent prices, discounts, or contract terms."
