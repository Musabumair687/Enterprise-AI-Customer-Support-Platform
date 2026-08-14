"""Billing and refund inquiry agent."""
from app.agents.base import SpecializedAgent
class BillingAgent(SpecializedAgent):
    name = "billing_agent"
    allowed_tools = frozenset({"get_invoice", "search_invoices", "get_payment_status", "get_refund_status", "knowledge_base_search"})
    system_prompt = "You are Corvex billing support. Explain billing or refund policy clearly. Never issue a refund or invent account facts; request an invoice identifier when needed."
