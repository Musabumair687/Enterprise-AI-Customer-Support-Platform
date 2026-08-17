"""Shared safe response behavior for Phase 10 specialized agents."""

import json
from typing import Any

from langchain_core.messages import HumanMessage

from app.core.logging import get_logger
from app.database.database import SessionLocal
from app.llm import LLMService
from app.memory.memory_manager import MemoryManager
from app.schemas.supervisor import AgentResult
from app.state.chat_state import ChatState
from app.tools.registry import invoke_tool
from app.tools.schemas import CustomerCRMProfileInput, CustomerLookupInput, EmployeeSearchInput, InvoiceSearchInput, KnownIssueSearchInput, ProductListInput


class SpecializedAgent:
    """A narrowly scoped response agent; subclasses declare their prompt and tool allow-list."""

    name: str
    system_prompt: str
    allowed_tools: frozenset[str]

    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()
        self.logger = get_logger()

    def __call__(self, state: ChatState) -> dict[str, object]:
        message = next((item.content.strip() for item in reversed(state["messages"])
                        if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()), "")
        if not message:
            return {"agent": self.name, "current_agent": self.name, "response": "Please share your question so I can help.",
                    "agent_results": self._results(state, "failed", "No customer message was available."),
                    "metadata": {**state.get("metadata", {}), "agent_status": "empty_message"}}
        evidence = self._collect_evidence(state, message)
        if evidence and evidence[0].get("status") == "needs_input":
            finding = str(evidence[0]["message"])
            return {"agent": self.name, "current_agent": self.name, "response": finding,
                    "agent_results": self._results(state, "needs_input", finding, evidence),
                    "metadata": {**state.get("metadata", {}), "agent_status": "needs_input"}}
        failures = [item for item in evidence if item.get("status") == "error"]
        if failures:
            finding = "I couldn't retrieve the information needed for this investigation."
            return {"agent": self.name, "current_agent": self.name, "response": finding,
                    "agent_results": self._results(state, "failed", finding, evidence, error=str(failures[0].get("message"))),
                    "metadata": {**state.get("metadata", {}), "agent_status": "tool_error"}}
        try:
            memory_context = MemoryManager.format_context(state)
            handoff = self._handoff_context(state, evidence)
            context = "\n\n".join(part for part in (memory_context, handoff) if part)
            system_prompt = f"{self.system_prompt}\n\n{context}" if context else self.system_prompt
            response = self.llm_service.generate(message, system_prompt=system_prompt, max_tokens=512)
        except Exception:
            self.logger.warning("Specialized agent unavailable | session_id=%s agent=%s", state["session_id"], self.name)
            return {"agent": self.name, "current_agent": self.name,
                    "response": "I'm sorry, I couldn't complete that request right now. Please try again shortly.",
                    "agent_results": self._results(state, "failed", "The specialist service was unavailable.", evidence),
                    "metadata": {**state.get("metadata", {}), "agent_status": "provider_error",
                                 "allowed_tools": sorted(self.allowed_tools)}}
        return {"agent": self.name, "current_agent": self.name, "response": response.content,
                "agent_results": self._results(state, "completed", response.content, evidence),
                "metadata": {**state.get("metadata", {}), "agent_status": "success",
                             "allowed_tools": sorted(self.allowed_tools)}}

    def _results(self, state: ChatState, status: str, finding: str, evidence: list[dict[str, object]] | None = None, error: str | None = None) -> dict[str, dict[str, object]]:
        results = dict(state.get("agent_results", {}))
        result = AgentResult(status=status, finding=finding, task=state.get("task"), evidence=evidence or [], error=error)
        results[self.name] = result.model_dump()
        return results

    def _collect_evidence(self, state: ChatState, message: str) -> list[dict[str, object]]:
        """Run one domain-appropriate, read-only lookup; never invoke write-capable tools."""
        customer_id = state.get("customer_id")
        if self.name in {"billing_agent", "customer_agent", "sales_agent"} and customer_id is None:
            return [{"status": "needs_input", "message": "Please provide authenticated customer account context so I can investigate this safely."}]
        try:
            with SessionLocal() as db:
                if self.name == "billing_agent":
                    output = invoke_tool("search_invoices", self.name, db, InvoiceSearchInput(customer_id=customer_id))
                    tool = "search_invoices"
                elif self.name == "customer_agent":
                    output = invoke_tool("customer_lookup", self.name, db, CustomerLookupInput(customer_id=customer_id))
                    tool = "customer_lookup"
                elif self.name == "sales_agent":
                    output = invoke_tool("get_customer_crm_profile", self.name, db, CustomerCRMProfileInput(customer_id=customer_id))
                    tool = "get_customer_crm_profile"
                elif self.name == "technical_agent":
                    output = invoke_tool("search_known_issues", self.name, db, KnownIssueSearchInput(query=message))
                    tool = "search_known_issues"
                elif self.name == "product_agent":
                    output = invoke_tool("list_products", self.name, db, ProductListInput())
                    tool = "list_products"
                elif self.name == "escalation_agent":
                    output = invoke_tool("find_support_agent", self.name, db, EmployeeSearchInput(query="support"))
                    tool = "find_support_agent"
                else:
                    return []
            return [{"tool": tool, "status": "success", "data": self._serialize(output)}]
        except Exception as exc:
            self.logger.warning("Specialist tool lookup failed | session_id=%s agent=%s", state["session_id"], self.name)
            return [{"status": "error", "message": str(exc)}]

    @staticmethod
    def _serialize(value: Any) -> object:
        if isinstance(value, list):
            return [SpecializedAgent._serialize(item) for item in value]
        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")
        return value

    @staticmethod
    def _handoff_context(state: ChatState, evidence: list[dict[str, object]]) -> str:
        return "\n".join((
            f"Supervisor task:\n{state.get('task') or 'Address the request within your domain.'}",
            f"Prior specialist results (do not repeat their work):\n{json.dumps(state.get('agent_results', {}), default=str)}",
            f"Authoritative read-only evidence:\n{json.dumps(evidence, default=str)}",
        ))
