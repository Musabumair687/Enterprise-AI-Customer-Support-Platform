"""
Typed contracts shared by the tool layer.

These schemas deliberately expose only fields an agent needs to answer a
support request or confirm an action.  Pydantic validates arguments before a
tool reaches a service and provides a stable JSON-friendly output shape for
LLM function calling, HTTP adapters, and tests.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.api import TicketCreate, TicketUpdate


class ToolModel(BaseModel):
    """Base model that can serialize SQLAlchemy-backed values safely."""

    model_config = ConfigDict(from_attributes=True)


class CustomerLookupInput(BaseModel):
    customer_id: int = Field(gt=0)


class CustomerSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=255)
    limit: int = Field(default=10, ge=1, le=50)


class CustomerToolOutput(ToolModel):
    customer_id: int
    external_id: str | None
    name: str
    email: str
    company: str | None
    subscription_plan: str | None
    status: str
    support_tier: str | None
    account_manager: str | None
    renewal_date: date | None


class TicketLookupInput(BaseModel):
    ticket_id: int = Field(gt=0)


class TicketSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=255)
    customer_id: int | None = Field(default=None, gt=0)
    limit: int = Field(default=10, ge=1, le=50)


class TicketCreateInput(TicketCreate):
    """The existing API validation contract, reused for agent-created tickets."""


class TicketUpdateInput(TicketUpdate):
    ticket_id: int = Field(gt=0)


class TicketToolOutput(ToolModel):
    ticket_id: int
    external_id: str | None
    customer_id: int
    title: str
    description: str
    status: str
    priority: str
    category: str | None
    assigned_agent_name: str | None
    is_escalated: bool
    escalation_reason: str | None
    created_at: datetime
    updated_at: datetime


class InvoiceLookupInput(BaseModel):
    invoice_id: int | None = Field(default=None, gt=0)
    invoice_number: str | None = Field(default=None, min_length=1, max_length=100)

    @model_validator(mode="after")
    def require_exactly_one_identifier(self) -> "InvoiceLookupInput":
        """Avoid silently preferring one identifier when callers provide two."""
        if (self.invoice_id is None) == (self.invoice_number is None):
            raise ValueError("Provide exactly one of invoice_id or invoice_number.")
        return self


class InvoiceSearchInput(BaseModel):
    customer_id: int | None = Field(default=None, gt=0)
    query: str | None = Field(default=None, min_length=1, max_length=100)
    limit: int = Field(default=10, ge=1, le=50)


class BillingToolOutput(ToolModel):
    invoice_id: int
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


class CustomerCRMProfileInput(CustomerLookupInput):
    conversation_limit: int = Field(default=5, ge=1, le=25)


class ConversationToolOutput(ToolModel):
    conversation_id: int
    ticket_id: int | None
    sender_role: str
    content: str
    created_at: datetime


class CustomerCRMProfileOutput(BaseModel):
    customer: CustomerToolOutput
    recent_conversations: list[ConversationToolOutput]


class ProductLookupInput(BaseModel):
    product_id: int = Field(gt=0)


class ProductListInput(BaseModel):
    active_only: bool = True
    limit: int = Field(default=20, ge=1, le=100)


class ProductToolOutput(ToolModel):
    product_id: int
    name: str
    description: str | None
    version: str | None
    is_active: bool


class KnownIssueSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=255)
    product_id: int | None = Field(default=None, gt=0)
    include_resolved: bool = False
    limit: int = Field(default=10, ge=1, le=50)


class KnownIssueToolOutput(ToolModel):
    issue_id: int
    title: str
    description: str
    severity: str
    status: str
    workaround: str | None
    product_id: int | None


class EmployeeLookupInput(BaseModel):
    employee_id: int = Field(gt=0)


class EmployeeSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=150)
    active_only: bool = True
    limit: int = Field(default=10, ge=1, le=50)


class EmployeeToolOutput(ToolModel):
    employee_id: int
    name: str
    email: str
    role: str
    is_active: bool


class EscalateTicketInput(BaseModel):
    ticket_id: int = Field(gt=0)
    reason: str = Field(min_length=1, max_length=2_000)
    assigned_employee_id: int | None = Field(default=None, gt=0)


class AssignTicketInput(BaseModel):
    ticket_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)


class KnowledgeBaseSearchInput(BaseModel):
    query: str = Field(min_length=1, max_length=2_000)
    candidate_k: int = Field(default=20, ge=1, le=50)
    final_k: int = Field(default=5, ge=1, le=10)

    @model_validator(mode="after")
    def final_k_must_not_exceed_candidate_k(self) -> "KnowledgeBaseSearchInput":
        if self.final_k > self.candidate_k:
            raise ValueError("final_k cannot exceed candidate_k.")
        return self


class KnowledgeBaseResult(ToolModel):
    chunk_id: str
    score: float
    source: str
    section: str
    text: str


class KnowledgeBaseSearchOutput(BaseModel):
    context: str
    results: list[KnowledgeBaseResult]
