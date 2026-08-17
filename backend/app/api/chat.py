"""Customer-facing entry point for the bounded multi-agent support workflow."""

from fastapi import APIRouter

from app.graph.workflow import CustomerSupportWorkflow
from app.schemas.api import ChatRequest, ChatResponse
from app.schemas.response import APIResponse


router = APIRouter(prefix="/chat", tags=["AI Support"])
workflow = CustomerSupportWorkflow()


@router.post("", response_model=APIResponse[ChatResponse])
def chat(request: ChatRequest) -> APIResponse[ChatResponse]:
    """Run one request through memory, supervision, and only needed specialists."""
    state = workflow.invoke(request.message, session_id=request.session_id, customer_id=request.customer_id)
    results = state.get("agent_results", {})
    return APIResponse(
        success=True,
        message="Support request processed.",
        data=ChatResponse(
            response=state.get("response") or "I couldn't complete your request right now.",
            session_id=state["session_id"],
            agents_used=list(results),
            escalated="escalation_agent" in results,
        ),
    )
