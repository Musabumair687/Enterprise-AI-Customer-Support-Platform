"""Stable contracts for the human-escalation workflow."""

from datetime import datetime

from pydantic import BaseModel, Field


class EscalationTicket(BaseModel):
    ticket_id: int
    external_id: str
    status: str
    department: str
    priority: str
    assigned_employee_id: int | None = None
    assigned_employee_name: str | None = None


class NotificationResult(BaseModel):
    channel: str = "dashboard"
    sent: bool = True
    message: str
    sent_at: datetime


class EscalationRequest(BaseModel):
    customer_id: int = Field(gt=0)
    issue: str = Field(min_length=1, max_length=8_000)
    reason: str = Field(min_length=1, max_length=2_000)
    department: str = Field(min_length=1, max_length=100)
    priority: str = Field(default="high", pattern="^(medium|high|urgent)$")
