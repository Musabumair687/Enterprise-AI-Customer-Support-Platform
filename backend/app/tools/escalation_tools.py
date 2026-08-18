"""Controlled ticket-routing actions for human escalation workflows."""

from sqlalchemy.orm import Session

from app.services.employee_service import get_employee
from app.services.ticket_service import get_ticket, update_ticket
from app.tools.errors import ToolNotFoundError, ToolOperationError
from app.tools.schemas import AssignTicketInput, EscalateTicketInput, TicketToolOutput
from app.tools.ticket_tools import serialize_ticket


def assign_ticket_tool(db: Session, tool_input: AssignTicketInput) -> TicketToolOutput:
    """Assign a ticket to an active employee after caller confirmation."""
    ticket = get_ticket(db, tool_input.ticket_id)
    if ticket is None:
        raise ToolNotFoundError(f"Ticket {tool_input.ticket_id} was not found.")
    employee = get_employee(db, tool_input.employee_id)
    if employee is None:
        raise ToolNotFoundError(f"Employee {tool_input.employee_id} was not found.")
    if not employee.is_active:
        raise ToolOperationError(f"Employee {tool_input.employee_id} is not active.")
    updated, error = update_ticket(db, ticket, {"assigned_employee_id": employee.id, "assigned_agent_name": employee.name, "status": "assigned"})
    if error or updated is None:
        raise ToolOperationError(error or "Ticket assignment failed.")
    return serialize_ticket(updated)


def escalate_ticket_tool(db: Session, tool_input: EscalateTicketInput) -> TicketToolOutput:
    """Mark a ticket escalated, retain the reason in its resolution history, and optionally assign it."""
    ticket = get_ticket(db, tool_input.ticket_id)
    if ticket is None:
        raise ToolNotFoundError(f"Ticket {tool_input.ticket_id} was not found.")
    values: dict[str, object] = {"is_escalated": True, "priority": "urgent", "escalation_reason": tool_input.reason}
    prior_resolution = ticket.resolution.strip() if ticket.resolution else ""
    values["resolution"] = f"{prior_resolution}\n\nEscalation reason: {tool_input.reason}".strip()
    if tool_input.assigned_employee_id is not None:
        employee = get_employee(db, tool_input.assigned_employee_id)
        if employee is None:
            raise ToolNotFoundError(f"Employee {tool_input.assigned_employee_id} was not found.")
        if not employee.is_active:
            raise ToolOperationError(f"Employee {tool_input.assigned_employee_id} is not active.")
        values.update(assigned_employee_id=employee.id, assigned_agent_name=employee.name, status="assigned")
    updated, error = update_ticket(db, ticket, values)
    if error or updated is None:
        raise ToolOperationError(error or "Ticket escalation failed.")
    return serialize_ticket(updated)
