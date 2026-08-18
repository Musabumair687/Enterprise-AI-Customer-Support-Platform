"""Notification boundary for human handoffs; currently an in-process mock."""

from datetime import UTC, datetime

from app.schemas.escalation_schema import NotificationResult


class NotificationService:
    def notify_customer(self, *, ticket_id: str, employee_name: str | None, department: str, priority: str) -> NotificationResult:
        owner = employee_name or f"the {department} team"
        eta = "as soon as possible" if priority == "urgent" else "within 2 business hours"
        return NotificationResult(
            message=f"Your issue has been assigned to {owner}. Ticket ID: {ticket_id}. Expected response: {eta}.",
            sent_at=datetime.now(UTC),
        )
