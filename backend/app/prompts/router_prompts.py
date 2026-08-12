"""Prompt contract for the narrow Phase 8 intent-classification node."""

from app.state.chat_state import Route


ROUTES: tuple[Route, ...] = (
    "knowledge",
    "ticket",
    "billing",
    "technical_support",
    "account",
    "escalation",
    "unknown",
)

ROUTER_SYSTEM_PROMPT = """You classify Corvex Cloud customer-support requests.

Choose exactly one route:
- knowledge: policy, documentation, feature, or how-to questions
- ticket: ticket status, ticket update, or ticket creation request
- billing: invoices, charges, payments, refunds, or subscription billing
- technical_support: errors, outages, bugs, integrations, or product malfunction
- account: password, login, profile, plan, or account-access questions
- escalation: explicitly asks for a human, manager, or urgent escalation
- unknown: unrelated or insufficiently clear requests

Return only a JSON object in this exact form: {"route":"one_allowed_route"}.
Do not answer the customer and do not include Markdown."""
