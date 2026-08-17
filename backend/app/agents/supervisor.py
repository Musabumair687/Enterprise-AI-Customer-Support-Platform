"""Sequential, bounded orchestration for the specialized support agents."""

import json
import re
from typing import Any

from langchain_core.messages import HumanMessage
from app.llm import LLMService
from app.prompts.supervisor_prompts import FINAL_RESPONSE_SYSTEM_PROMPT, SUPERVISOR_SYSTEM_PROMPT
from app.schemas.supervisor import SupervisorDecision
from app.state.chat_state import ChatState


MAX_AGENT_STEPS = 5
_AGENT_ORDER = ("customer_agent", "billing_agent", "technical_agent", "product_agent", "sales_agent", "escalation_agent")


class SupervisorAgent:
    """Pick one worker at a time and aggregate their results into the final answer."""

    name = "supervisor"

    def __init__(self, llm_service: LLMService | None = None, max_agent_steps: int = MAX_AGENT_STEPS, available_agents: frozenset[str] | None = None) -> None:
        self.llm_service = llm_service or LLMService()
        self.max_agent_steps = max_agent_steps
        self.available_agents = available_agents or frozenset(_AGENT_ORDER)

    def set_available_agents(self, available_agents: frozenset[str]) -> None:
        """Keep routing constrained to nodes actually registered in the graph."""
        self.available_agents = available_agents

    def __call__(self, state: ChatState) -> dict[str, object]:
        results = state.get("agent_results", {})
        if state.get("agent_step_count", 0) >= self.max_agent_steps:
            return self._complete(state, "The collaboration safety limit was reached; a human follow-up may be needed.")
        decision = self._decide(state, results)
        if decision.status == "complete":
            return self._complete(state, decision.reason)
        return {
            "current_agent": self.name,
            "next_agent": decision.next_agent,
            "task": decision.task,
            "subtasks": self._subtasks(state, results, decision),
            "metadata": {**state.get("metadata", {}), "supervisor_status": "continue", "supervisor_reason": decision.reason},
        }

    def _decide(self, state: ChatState, results: dict[str, dict[str, object]]) -> SupervisorDecision:
        failed = [name for name, result in results.items() if result.get("status") == "failed"]
        if failed:
            if "escalation_agent" not in results:
                return SupervisorDecision(next_agent="escalation_agent", task="Arrange an appropriate human handoff for the unresolved support issue.", reason="A specialist could not complete its investigation.", status="continue")
            return SupervisorDecision(reason="The required investigations have completed or were handed off.", status="complete")
        if any(result.get("status") == "needs_input" for result in results.values()):
            return SupervisorDecision(reason="Additional customer account context is required before continuing safely.", status="complete")
        try:
            message = self._latest_message(state)
            payload = {"customer_request": message, "intent": str(state.get("intent") or ""), "agent_results": results, "completed_agents": list(results)}
            content = self.llm_service.generate(json.dumps(payload), system_prompt=SUPERVISOR_SYSTEM_PROMPT, temperature=0, max_tokens=300).content
            return self._parse_decision(content, results)
        except Exception:
            return self._fallback_decision(state, results)

    def _parse_decision(self, content: str, results: dict[str, dict[str, object]]) -> SupervisorDecision:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        payload: Any = json.loads(match.group(0) if match else content)
        decision = SupervisorDecision.model_validate(payload)
        if decision.next_agent not in self.available_agents or decision.next_agent in results:
            return self._fallback_decision(state, results)
        return decision

    def _fallback_decision(self, state: ChatState, results: dict[str, dict[str, object]]) -> SupervisorDecision:
        text = self._latest_message(state).lower()
        candidates: list[tuple[str, str]] = []
        if any(word in text for word in ("charged", "charge", "invoice", "payment", "refund", "billing")):
            candidates.append(("billing_agent", "Investigate the customer's billing or payment concern."))
        if any(word in text for word in ("api", "error", "not working", "login", "authentication", "technical", "bug")):
            candidates.append(("technical_agent", "Investigate the reported technical problem."))
        if any(word in text for word in ("plan", "account", "profile", "subscription", "current plan")):
            candidates.append(("customer_agent", "Check the customer account information relevant to the request."))
        if any(word in text for word in ("upgrade", "pricing", "price", "purchase", "enterprise")):
            candidates.append(("sales_agent", "Provide verified plan or upgrade guidance."))
        if any(word in text for word in ("human", "representative", "escalate", "complaint")):
            candidates.append(("escalation_agent", "Arrange or explain the human support handoff."))
        if not candidates:
            candidates.append(("product_agent", "Answer the product or documentation question."))
        for agent, task in candidates:
            if agent in self.available_agents and agent not in results:
                return SupervisorDecision(next_agent=agent, task=task, reason="This domain is required by the customer request.", status="continue")
        return SupervisorDecision(reason="All required specialist investigations have completed.", status="complete")

    def _complete(self, state: ChatState, reason: str) -> dict[str, object]:
        results = state.get("agent_results", {})
        response = self._final_response(state, results, reason)
        return {"current_agent": self.name, "next_agent": None, "task": None, "response": response,
                "metadata": {**state.get("metadata", {}), "supervisor_status": "complete", "supervisor_reason": reason}}

    def _final_response(self, state: ChatState, results: dict[str, dict[str, object]], reason: str) -> str:
        if not results:
            return "I need a little more detail to route your request to the right support specialist."
        try:
            prompt = json.dumps({"customer_request": self._latest_message(state), "agent_results": results, "completion_reason": reason})
            return self.llm_service.generate(prompt, system_prompt=FINAL_RESPONSE_SYSTEM_PROMPT, temperature=0.2, max_tokens=400).content
        except Exception:
            findings = [str(result.get("finding") or result.get("response") or "Investigation completed.") for result in results.values()]
            return " ".join(findings)

    @staticmethod
    def _latest_message(state: ChatState) -> str:
        return next((item.content.strip() for item in reversed(state.get("messages", [])) if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()), "")

    @staticmethod
    def _subtasks(state: ChatState, results: dict[str, dict[str, object]], decision: SupervisorDecision) -> list[dict[str, object]]:
        existing = list(state.get("subtasks", []))
        if decision.next_agent:
            existing.append({"agent": decision.next_agent, "task": decision.task, "status": "pending"})
        return existing
