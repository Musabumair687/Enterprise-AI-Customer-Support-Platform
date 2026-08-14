"""Product information and feature-request agent."""
from app.agents.base import SpecializedAgent
class ProductAgent(SpecializedAgent):
    name = "product_agent"
    allowed_tools = frozenset({"knowledge_base_search", "get_product", "list_products"})
    system_prompt = "You are Corvex product support. Answer product questions only with verified information and record feature requests without promising delivery dates."
