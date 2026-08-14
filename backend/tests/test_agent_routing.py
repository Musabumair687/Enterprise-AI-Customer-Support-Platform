"""Offline checks for Phase 10 routing and least-privilege tool policy."""

import unittest

from app.graph.routes import INTENT_AGENT_MAP, route_for_intent
from app.schemas.intent import Intent
from app.tools.registry import get_tools_for_agent


class AgentRoutingTests(unittest.TestCase):
    def test_every_supported_intent_has_the_expected_agent(self) -> None:
        self.assertEqual(set(INTENT_AGENT_MAP), set(Intent))
        self.assertEqual(route_for_intent(Intent.REFUND), "billing_agent")
        self.assertEqual(route_for_intent(Intent.COMPLAINT), "escalation_agent")
        self.assertEqual(route_for_intent(None), "customer_agent")

    def test_tool_permissions_are_scoped_to_each_agent(self) -> None:
        actual = {agent: {tool.name for tool in get_tools_for_agent(agent)} for agent in (
            "customer_agent", "billing_agent", "technical_agent", "product_agent",
            "escalation_agent", "sales_agent",
        )}
        self.assertEqual(actual["customer_agent"], {"customer_lookup", "customer_search"})
        self.assertEqual(actual["billing_agent"], {"get_invoice", "search_invoices", "get_payment_status", "get_refund_status", "knowledge_base_search"})
        self.assertEqual(actual["technical_agent"], {"get_ticket", "search_tickets", "search_known_issues", "knowledge_base_search"})
        self.assertEqual(actual["product_agent"], {"get_product", "list_products", "knowledge_base_search"})
        self.assertEqual(actual["escalation_agent"], {"find_employee", "find_employee_by_skill", "find_support_agent", "assign_ticket", "escalate_ticket"})
        self.assertEqual(actual["sales_agent"], {"customer_lookup", "get_customer_crm_profile", "get_product", "list_products", "knowledge_base_search"})


if __name__ == "__main__":
    unittest.main()
