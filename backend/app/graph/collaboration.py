"""Conditional routing policy for the bounded supervisor/worker collaboration loop."""

from app.state.chat_state import ChatState


def route_supervisor(state: ChatState) -> str:
    """Send the graph to one validated worker, or persist the supervisor's final reply."""
    if state.get("next_agent") is None:
        return "save_memory"
    return state["next_agent"]


def route_after_confidence(state: ChatState) -> str:
    """Send low-confidence turns to the handoff node exactly once."""
    if state.get("escalation_required") and "escalation_agent" not in state.get("agent_results", {}):
        return "escalation_agent"
    return "supervisor"


def record_agent_step(state: ChatState) -> dict[str, object]:
    """Increment the collaboration counter only after a specialist has run."""
    completed_agent = state.get("current_agent")
    subtasks = list(state.get("subtasks", []))
    for subtask in reversed(subtasks):
        if subtask.get("agent") == completed_agent and subtask.get("status") == "pending":
            result = state.get("agent_results", {}).get(completed_agent or "", {})
            subtask["status"] = str(result.get("status", "completed"))
            break
    return {"agent_step_count": state.get("agent_step_count", 0) + 1, "subtasks": subtasks}
