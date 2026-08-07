"""Pydantic schemas used by the Version 1 REST API."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None
    name: str
    email: str
    company: str | None
    phone: str | None
    country: str | None
    timezone: str | None
    subscription_plan: str | None
    status: str
    registration_date: date | None
    renewal_date: date | None
    last_login: datetime | None
    preferred_language: str | None
    support_tier: str | None
    account_manager: str | None
    monthly_revenue: Decimal | None
    lifetime_value: Decimal | None
    created_at: datetime
    updated_at: datetime


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    version: str | None
    is_active: bool
    created_at: datetime


class BillingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    invoice_number: str | None
    plan: str | None
    amount: Decimal
    currency: str
    status: str
    record_type: str
    payment_method: str | None
    due_date: date | None
    paid_date: date | None
    refund_status: str | None
    created_at: datetime


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    ticket_id: int | None
    session_id: str
    sender_role: str
    content: str
    created_at: datetime


class TicketBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    status: str = Field(default="open", max_length=30)
    priority: str = Field(default="medium", max_length=30)
    department: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=80)
    assigned_agent_name: str | None = Field(default=None, max_length=150)
    resolution: str | None = None
    sentiment: str | None = Field(default=None, max_length=30)
    resolution_time_hours: Decimal | None = Field(default=None, ge=0)
    is_escalated: bool = False
    assigned_employee_id: int | None = None
    product_id: int | None = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        """Accept the supported ticket priorities, including imported 'normal' values."""
        normalized = value.strip().lower()
        normalized = "medium" if normalized == "normal" else normalized
        if normalized not in {"low", "medium", "high", "urgent"}:
            raise ValueError("Priority must be one of: low, medium, high, urgent.")
        return normalized

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """Limit tickets to the workflow states supported by the platform."""
        normalized = value.strip().lower().replace(" ", "_")
        if normalized not in {"open", "pending", "in_progress", "resolved", "closed"}:
            raise ValueError("Status must be one of: open, pending, in_progress, resolved, closed.")
        return normalized


class TicketCreate(TicketBase):
    customer_id: int
    external_id: str | None = Field(default=None, max_length=50)


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    status: str | None = Field(default=None, max_length=30)
    priority: str | None = Field(default=None, max_length=30)
    department: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=80)
    assigned_agent_name: str | None = Field(default=None, max_length=150)
    resolution: str | None = None
    sentiment: str | None = Field(default=None, max_length=30)
    resolution_time_hours: Decimal | None = Field(default=None, ge=0)
    is_escalated: bool | None = None
    customer_id: int | None = None
    assigned_employee_id: int | None = None
    product_id: int | None = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.strip().lower()
        normalized = "medium" if normalized == "normal" else normalized
        if normalized not in {"low", "medium", "high", "urgent"}:
            raise ValueError("Priority must be one of: low, medium, high, urgent.")
        return normalized

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.strip().lower().replace(" ", "_")
        if normalized not in {"open", "pending", "in_progress", "resolved", "closed"}:
            raise ValueError("Status must be one of: open, pending, in_progress, resolved, closed.")
        return normalized

    @model_validator(mode="after")
    def reject_null_required_fields(self) -> "TicketUpdate":
        """Keep required database columns from being cleared by an update."""
        required_fields = {"title", "description", "status", "priority", "is_escalated"}
        null_fields = sorted(
            field
            for field in self.model_fields_set & required_fields
            if getattr(self, field) is None
        )
        if null_fields:
            raise ValueError(f"These fields cannot be null: {', '.join(null_fields)}.")
        return self


class TicketRead(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None
    customer_id: int
    created_at: datetime
    updated_at: datetime
