"""The fixed Phase 10 policy mapping business intents to specialized agents."""

from app.schemas.intent import Intent

INTENT_AGENT_MAP: dict[Intent, str] = {
    Intent.BILLING: "billing_agent",
    Intent.REFUND: "billing_agent",
    Intent.TECHNICAL_SUPPORT: "technical_agent",
    Intent.GENERAL_QUESTION: "product_agent",
    Intent.FEATURE_REQUEST: "product_agent",
    Intent.SALES: "sales_agent",
    Intent.HUMAN_AGENT: "escalation_agent",
    Intent.COMPLAINT: "escalation_agent",
}


def route_for_intent(intent: Intent | None) -> str:
    """Return the designated agent, defaulting unknown classifications to customer care."""
    return INTENT_AGENT_MAP.get(intent, "customer_agent")
