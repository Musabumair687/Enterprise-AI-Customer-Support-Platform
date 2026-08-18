"""Focused checks for Phase 13 human-handoff policy and routing."""

from langchain_core.messages import HumanMessage

from app.config.escalation_rules import classify_department, escalation_reason
from app.core.confidence import evaluate_confidence
from app.graph.collaboration import route_after_confidence


def test_explicit_human_request_overrides_other_confidence() -> None:
    state = {"messages": [HumanMessage(content="I need a manager and a human now")], "agent_results": {"product_agent": {"status": "completed"}}, "metadata": {}}
    decision = evaluate_confidence(state)  # type: ignore[arg-type]
    assert decision.escalation_required
    assert decision.confidence_score == 0.85
    assert "explicitly" in decision.reason.lower()  # type: ignore[union-attr]


def test_sensitive_large_refund_routes_to_finance() -> None:
    message = "Refund my $50,000 invoice immediately"
    assert escalation_reason(message, 0.9) is not None
    assert classify_department(message) == "Finance"


def test_low_confidence_routes_to_escalation_node_once() -> None:
    assert route_after_confidence({"escalation_required": True, "agent_results": {}}) == "escalation_agent"  # type: ignore[arg-type]
    assert route_after_confidence({"escalation_required": True, "agent_results": {"escalation_agent": {}}}) == "supervisor"  # type: ignore[arg-type]
