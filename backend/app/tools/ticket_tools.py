"""
Ticket tools for retrieving and safely changing support cases.

Read tools give agents current case context.  Write tools reuse the existing
Pydantic ticket validation and ticket service relation checks, so an LLM cannot
create a ticket with an invalid workflow status or reference a non-existent
customer, employee, or product.  The returned ``ticket_id`` confirms successful
creation or update to the caller.
"""

from sqlalchemy.orm import Session

from app.services.ticket_service import create_ticket, get_ticket, search_tickets, update_ticket
from app.tools.errors import ToolNotFoundError, ToolOperationError
from app.tools.schemas import TicketCreateInput, TicketLookupInput, TicketSearchInput, TicketToolOutput, TicketUpdateInput


def serialize_ticket(ticket) -> TicketToolOutput:
    """Convert a ticket model to the stable agent-facing output contract."""
    return TicketToolOutput(
        ticket_id=ticket.id, external_id=ticket.external_id, customer_id=ticket.customer_id,
        title=ticket.title, description=ticket.description, status=ticket.status, priority=ticket.priority,
        category=ticket.category, assigned_agent_name=ticket.assigned_agent_name,
        is_escalated=ticket.is_escalated, escalation_reason=ticket.escalation_reason,
        created_at=ticket.created_at, updated_at=ticket.updated_at,
    )


def get_ticket_tool(db: Session, tool_input: TicketLookupInput) -> TicketToolOutput:
    """Return one ticket and its current workflow state."""
    ticket = get_ticket(db, tool_input.ticket_id)
    if ticket is None:
        raise ToolNotFoundError(f"Ticket {tool_input.ticket_id} was not found.")
    return serialize_ticket(ticket)


def search_tickets_tool(db: Session, tool_input: TicketSearchInput) -> list[TicketToolOutput]:
    """Search tickets by title/description, optionally restricted to one customer."""
    return [serialize_ticket(ticket) for ticket in search_tickets(db, tool_input.query, tool_input.customer_id, tool_input.limit)]


def create_ticket_tool(db: Session, tool_input: TicketCreateInput) -> TicketToolOutput:
    """Create a validated support ticket and return its new ticket ID."""
    ticket, error = create_ticket(db, tool_input.model_dump())
    if error or ticket is None:
        raise ToolOperationError(error or "Ticket creation failed.")
    return serialize_ticket(ticket)


def update_ticket_tool(db: Session, tool_input: TicketUpdateInput) -> TicketToolOutput:
    """Update only fields explicitly supplied by the caller."""
    ticket = get_ticket(db, tool_input.ticket_id)
    if ticket is None:
        raise ToolNotFoundError(f"Ticket {tool_input.ticket_id} was not found.")
    values = tool_input.model_dump(exclude={"ticket_id"}, exclude_unset=True)
    updated_ticket, error = update_ticket(db, ticket, values)
    if error or updated_ticket is None:
        raise ToolOperationError(error or "Ticket update failed.")
    return serialize_ticket(updated_ticket)
