"""Product-information agent grounded in approved product and documentation tools."""

from app.agents.base import SpecializedAgent


class ProductAgent(SpecializedAgent):
    """Answer product and feature questions without making unsupported claims."""

    name = "product_agent"
    allowed_tools = frozenset({"knowledge_base_search", "get_product", "list_products"})
    system_prompt = (
        "You are Corvex product support. Answer feature and product questions only "
        "from verified documentation or product data. Never invent availability, "
        "versions, integrations, or roadmap commitments."
    )
