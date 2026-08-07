"""Support-ticket REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import TicketCreate, TicketRead, TicketUpdate
from app.schemas.response import APIResponse
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("", response_model=APIResponse[list[TicketRead]])
def list_tickets(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[TicketRead]]:
    tickets = ticket_service.list_tickets(db, skip, limit)
    return APIResponse(success=True, message="Tickets retrieved successfully.", data=[TicketRead.model_validate(ticket) for ticket in tickets])


@router.get("/{ticket_id}", response_model=APIResponse[TicketRead])
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> APIResponse[TicketRead]:
    ticket = ticket_service.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found.")
    return APIResponse(success=True, message="Ticket retrieved successfully.", data=TicketRead.model_validate(ticket))


@router.post("", response_model=APIResponse[TicketRead], status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> APIResponse[TicketRead]:
    ticket, error = ticket_service.create_ticket(db, payload.model_dump())
    if error or ticket is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error or "Ticket could not be created.")
    return APIResponse(success=True, message="Ticket created successfully.", data=TicketRead.model_validate(ticket))


@router.put("/{ticket_id}", response_model=APIResponse[TicketRead])
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)) -> APIResponse[TicketRead]:
    ticket = ticket_service.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found.")
    updated_ticket, error = ticket_service.update_ticket(db, ticket, payload.model_dump(exclude_unset=True))
    if error or updated_ticket is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error or "Ticket could not be updated.")
    return APIResponse(success=True, message="Ticket updated successfully.", data=TicketRead.model_validate(updated_ticket))


@router.delete("/{ticket_id}", response_model=APIResponse[dict[str, int]])
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)) -> APIResponse[dict[str, int]]:
    ticket = ticket_service.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found.")
    ticket_service.delete_ticket(db, ticket)
    return APIResponse(success=True, message="Ticket deleted successfully.", data={"id": ticket_id})
