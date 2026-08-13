"""Offline unit and graph tests for Phase 9 intent classification."""

import unittest
from types import SimpleNamespace

from langchain_core.messages import HumanMessage

from app.graph.workflow import CustomerSupportWorkflow
from app.llm.schemas import LLMProviderName
from app.nodes.intent_classifier import IntentClassifierNode, parse_intent
from app.schemas.intent import Intent


class FakeLLMService:
    def __init__(self, intent: str) -> None:
        self.intent = intent

    def chat(self, request):
        return SimpleNamespace(content=f'{{"intent":"{self.intent}"}}', provider=LLMProviderName.GEMINI, model="fake-model", latency_ms=1.0)


class IntentClassifierTests(unittest.TestCase):
    def test_parses_only_allowed_intents(self) -> None:
        self.assertEqual(parse_intent('{"intent":"billing"}'), Intent.BILLING)
        self.assertEqual(parse_intent('```json\n{"intent":"refund"}\n```'), Intent.REFUND)
        self.assertIsNone(parse_intent('{"intent":"payment_issue"}'))
        self.assertIsNone(parse_intent('billing'))

    def test_node_records_intent_and_metadata(self) -> None:
        node = IntentClassifierNode(llm_service=FakeLLMService("technical_support"))
        result = node({"messages": [HumanMessage(content="CD-401 error")], "session_id": "test", "intent": None, "metadata": {}})
        self.assertEqual(result["intent"], Intent.TECHNICAL_SUPPORT)
        self.assertEqual(result["metadata"]["classification_status"], "success")

    def test_empty_message_skips_provider(self) -> None:
        node = IntentClassifierNode(llm_service=FakeLLMService("billing"))
        result = node({"messages": [HumanMessage(content=" ")], "session_id": "test", "intent": None, "metadata": {}})
        self.assertIsNone(result["intent"])
        self.assertEqual(result["metadata"]["classification_status"], "empty_message")

    def test_start_classifier_end_workflow(self) -> None:
        workflow = CustomerSupportWorkflow(IntentClassifierNode(llm_service=FakeLLMService("billing")))
        result = workflow.invoke("Why was I charged twice?", session_id="session-1")
        self.assertEqual(result["intent"], Intent.BILLING)
        self.assertEqual(result["session_id"], "session-1")


if __name__ == "__main__":
    unittest.main()
