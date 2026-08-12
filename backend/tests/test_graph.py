"""Offline integration test for the minimal Phase 8 LangGraph workflow."""

import unittest
from types import SimpleNamespace

from app.graph.workflow import CustomerSupportWorkflow
from app.llm.schemas import LLMProviderName
from app.nodes.router import RouterNode


class BillingLLM:
    def chat(self, request):
        return SimpleNamespace(content='{"route":"billing"}', provider=LLMProviderName.GROQ,
                               model="fake-model", latency_ms=1.0)


class GraphTests(unittest.TestCase):
    def test_start_router_end_workflow(self) -> None:
        workflow = CustomerSupportWorkflow(RouterNode(llm_service=BillingLLM()))
        result = workflow.invoke("Why was I charged twice?", session_id="session-1")
        self.assertEqual(result["route"], "billing")
        self.assertEqual(result["session_id"], "session-1")


if __name__ == "__main__":
    unittest.main()
