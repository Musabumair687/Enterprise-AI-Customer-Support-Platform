"""Create and route a human-support handoff once escalation policy requires it."""

from langchain_core.messages import HumanMessage

from app.agents.base import SpecializedAgent
from app.config.escalation_rules import classify_department, classify_priority
from app.database.database import SessionLocal
from app.schemas.escalation_schema import EscalationRequest
from app.services.assignment_service import AssignmentService
from app.services.notification_service import NotificationService
from app.services.ticket_service import create_ticket
from app.state.chat_state import ChatState


class EscalationAgent(SpecializedAgent):
    name = "escalation_agent"
    allowed_tools = frozenset({"find_employee", "find_employee_by_skill", "find_support_agent", "assign_ticket", "escalate_ticket"})
    system_prompt = "You manage human-support handoffs. Never claim a ticket or assignment that was not created."

    def __init__(self, *args, assignment_service: AssignmentService | None = None, notification_service: NotificationService | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.assignment_service = assignment_service or AssignmentService()
        self.notification_service = notification_service or NotificationService()

    def __call__(self, state: ChatState) -> dict[str, object]:
        message = self._latest_message(state)
        customer_id = state.get("customer_id")
        reason = state.get("escalation_reason") or "The customer requested human support."
        if not message or customer_id is None:
            return self._result(state, "I can arrange a human handoff, but I need authenticated customer account context first.", "needs_input", reason)
        department, priority = classify_department(message), classify_priority(message)
        request = EscalationRequest(customer_id=customer_id, issue=message, reason=reason, department=department, priority=priority)
        try:
            with SessionLocal() as db:
                employee = self.assignment_service.assign(db, request.department, request.issue)
                ticket, error = create_ticket(db, {"external_id": None, "customer_id": request.customer_id, "title": f"Human escalation: {request.issue[:220]}", "description": request.issue, "status": "assigned" if employee else "open", "priority": request.priority, "department": request.department, "assigned_employee_id": employee.id if employee else None, "assigned_agent_name": employee.name if employee else None, "is_escalated": True, "escalation_reason": request.reason})
                if error or ticket is None:
                    raise RuntimeError(error or "Ticket creation failed.")
                ticket.external_id = f"TK-{ticket.id:05d}"
                db.commit()
                db.refresh(ticket)
        except Exception:
            self.logger.exception("Escalation ticket creation failed | session_id=%s", state["session_id"])
            return self._result(state, "I couldn't complete the human handoff right now. Please try again shortly.", "failed", reason)
        notification = self.notification_service.notify_customer(ticket_id=ticket.external_id, employee_name=employee.name if employee else None, department=department, priority=priority)
        return self._result(
            state,
            notification.message,
            "completed",
            reason,
            ticket_id=ticket.id,
            employee={"id": employee.id, "name": employee.name, "department": department} if employee else None,
            ticket_reference=ticket.external_id,
        )

    @staticmethod
    def _latest_message(state: ChatState) -> str:
        return next((item.content.strip() for item in reversed(state.get("messages", [])) if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()), "")

    def _result(self, state: ChatState, response: str, status: str, reason: str, *, ticket_id: int | None = None, employee: dict[str, object] | None = None, ticket_reference: str | None = None) -> dict[str, object]:
        session_memory = dict(state.get("session_memory", {}))
        if ticket_reference:
            session_memory["ticket"] = ticket_reference
        return {"agent": self.name, "current_agent": self.name, "response": response, "ticket_id": ticket_id, "assigned_employee": employee, "session_memory": session_memory, "agent_results": self._results(state, status, response, [{"reason": reason, "ticket_id": ticket_id}]), "metadata": {**state.get("metadata", {}), "agent_status": status, "human_handoff": status == "completed"}}
