"""Offline tests for strict route parsing and the Phase 8 router node."""

import unittest
from types import SimpleNamespace

from langchain_core.messages import HumanMessage

from app.llm.schemas import LLMProviderName
from app.nodes.router import RouterNode, parse_route


class FakeLLMService:
    def __init__(self, route: str) -> None:
        self.route = route

    def chat(self, request):
        return SimpleNamespace(content=f'{{"route":"{self.route}"}}', provider=LLMProviderName.GEMINI,
                               model="fake-model", latency_ms=1.0)


class RouterTests(unittest.TestCase):
    def test_parses_only_allowed_routes(self) -> None:
        self.assertEqual(parse_route('{"route":"billing"}'), "billing")
        self.assertEqual(parse_route('```json\n{"route":"ticket"}\n```'), "ticket")
        self.assertEqual(parse_route('{"route":"pizza"}'), "unknown")
        self.assertEqual(parse_route('billing'), "unknown")

    def test_node_updates_route(self) -> None:
        node = RouterNode(llm_service=FakeLLMService("technical_support"))
        result = node({"messages": [HumanMessage(content="CD-401 error")], "session_id": "test", "route": "unknown"})
        self.assertEqual(result, {"route": "technical_support"})

    def test_empty_message_skips_llm(self) -> None:
        node = RouterNode(llm_service=FakeLLMService("billing"))
        result = node({"messages": [HumanMessage(content="  ")], "session_id": "test", "route": "unknown"})
        self.assertEqual(result, {"route": "unknown"})


if __name__ == "__main__":
    unittest.main()
