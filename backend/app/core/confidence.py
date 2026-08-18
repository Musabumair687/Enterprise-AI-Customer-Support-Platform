"""Confidence evaluation node used by the human-escalation graph."""

from dataclasses import dataclass

from langchain_core.messages import HumanMessage

from app.config.escalation_rules import escalation_reason
from app.state.chat_state import ChatState


@dataclass(frozen=True, slots=True)
class ConfidenceEvaluation:
    confidence_score: float
    reason: str | None

    @property
    def escalation_required(self) -> bool:
        return self.reason is not None


def evaluate_confidence(state: ChatState) -> ConfidenceEvaluation:
    """Evaluate an auditable score without asking an LLM to judge its own certainty."""
    results = state.get("agent_results", {})
    failures = sum(result.get("status") == "failed" for result in results.values())
    needs_input = sum(result.get("status") == "needs_input" for result in results.values())
    configured = state.get("metadata", {}).get("confidence_score")
    if isinstance(configured, (int, float)):
        score = max(0.0, min(1.0, float(configured)))
    elif failures:
        score = 0.2
    elif needs_input:
        score = 0.45
    elif results:
        score = 0.85
    else:
        score = 0.45
    message = next((item.content.strip() for item in reversed(state.get("messages", []))
                    if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()), "")
    return ConfidenceEvaluation(score, escalation_reason(message, score, failures))


def confidence_node(state: ChatState) -> dict[str, object]:
    """Store the decision in graph state so every handoff is explainable."""
    decision = evaluate_confidence(state)
    return {
        "confidence_score": decision.confidence_score,
        "escalation_required": decision.escalation_required,
        "escalation_reason": decision.reason,
        "metadata": {**state.get("metadata", {}), "confidence_evaluated": True},
    }
