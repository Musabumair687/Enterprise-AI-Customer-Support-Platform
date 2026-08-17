"""Offline regression tests for Phase 12 supervisor collaboration."""

import unittest

from langchain_core.messages import HumanMessage

from app.agents.supervisor import SupervisorAgent
from app.agents.base import SpecializedAgent
from app.graph.builder import build_graph
from app.schemas.intent import Intent
from app.state.chat_state import ChatState


class FailingLLM:
    """Force deterministic supervisor fallback behavior in offline tests."""

    def generate(self, *args, **kwargs):
        raise RuntimeError("provider unavailable")


class SequenceLLM:
    def __init__(self, *contents: str) -> None:
        self.contents = list(contents)
        self.system_prompts: list[str] = []

    def generate(self, prompt, **kwargs):
        self.system_prompts.append(kwargs.get("system_prompt", ""))
        return type("Response", (), {"content": self.contents.pop(0)})()


class ContextAgent(SpecializedAgent):
    name = "technical_agent"
    system_prompt = "technical prompt"
    allowed_tools = frozenset()

    def _collect_evidence(self, state, message):
        return [{"tool": "search_known_issues", "status": "success", "data": []}]


class NoopMemory:
    def load_graph_state(self, state):
        return {}

    def save_graph_state(self, state):
        return {}


class FixedClassifier:
    def __call__(self, state):
        return {"intent": Intent.BILLING}


class CompletedAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, state):
        results = dict(state.get("agent_results", {}))
        results[self.name] = {"status": "completed", "finding": f"{self.name} completed."}
        return {"current_agent": self.name, "response": f"{self.name} completed.", "agent_results": results}


def state(message: str, **updates: object) -> ChatState:
    base: ChatState = {
        "messages": [HumanMessage(content=message)], "session_id": "test", "metadata": {},
        "agent_results": {}, "agent_step_count": 0, "subtasks": [], "intent": None,
    }
    base.update(updates)
    return base


class CollaborationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supervisor = SupervisorAgent(llm_service=FailingLLM())

    def test_multi_domain_request_is_sequenced_without_repeating_workers(self) -> None:
        first = self.supervisor(state("I was charged twice and my API authentication is not working."))
        self.assertEqual(first["next_agent"], "billing_agent")
        second = self.supervisor(state(
            "I was charged twice and my API authentication is not working.",
            agent_results={"billing_agent": {"status": "completed", "finding": "Duplicate charge found."}},
        ))
        self.assertEqual(second["next_agent"], "technical_agent")

    def test_specialist_failure_routes_to_human_escalation(self) -> None:
        result = self.supervisor(state(
            "My invoice is wrong.",
            agent_results={"billing_agent": {"status": "failed", "finding": "Database unavailable."}},
        ))
        self.assertEqual(result["next_agent"], "escalation_agent")

    def test_limit_completes_safely(self) -> None:
        result = self.supervisor(state("My API is broken.", agent_step_count=5))
        self.assertIsNone(result["next_agent"])
        self.assertEqual(result["metadata"]["supervisor_status"], "complete")

    def test_completed_single_domain_request_finishes(self) -> None:
        result = self.supervisor(state(
            "What is my current plan?",
            agent_results={"customer_agent": {"status": "completed", "finding": "Current plan reviewed."}},
        ))
        self.assertIsNone(result["next_agent"])

    def test_graph_returns_to_supervisor_between_specialists(self) -> None:
        graph = build_graph(
            intent_classifier=FixedClassifier(),
            agents={"billing_agent": CompletedAgent("billing_agent"), "technical_agent": CompletedAgent("technical_agent")},
            memory_manager=NoopMemory(),
            supervisor=self.supervisor,
        )
        result = graph.invoke(state("I was charged twice and my API authentication is not working."))
        self.assertEqual(result["agent_step_count"], 2)
        self.assertEqual(set(result["agent_results"]), {"billing_agent", "technical_agent"})
        self.assertIsNotNone(result["response"])

    def test_repeated_llm_route_falls_back_to_remaining_domain(self) -> None:
        supervisor = SupervisorAgent(llm_service=SequenceLLM(
            '{"next_agent":"billing_agent","task":"repeat","reason":"test","status":"continue"}'
        ))
        result = supervisor(state(
            "I was charged twice and my API is broken.",
            agent_results={"billing_agent": {"status": "completed", "finding": "billing complete"}},
        ))
        self.assertEqual(result["next_agent"], "technical_agent")

    def test_specialist_receives_supervisor_handoff_context(self) -> None:
        llm = SequenceLLM("Evidence-based technical response.")
        agent = ContextAgent(llm_service=llm)
        result = agent(state(
            "My API fails.", task="Investigate API authentication.",
            agent_results={"billing_agent": {"status": "completed", "finding": "No duplicate charge."}},
        ))
        self.assertEqual(result["agent_results"]["technical_agent"]["status"], "completed")
        self.assertIn("Supervisor task:\nInvestigate API authentication.", llm.system_prompts[0])
        self.assertIn("billing_agent", llm.system_prompts[0])

    def test_missing_account_context_completes_with_a_follow_up_request(self) -> None:
        result = self.supervisor(state(
            "What is my current plan?",
            agent_results={"customer_agent": {"status": "needs_input", "finding": "Please provide authenticated customer account context."}},
        ))
        self.assertIsNone(result["next_agent"])


if __name__ == "__main__":
    unittest.main()
