"""
===============================================================================
Database Models Module

Purpose:
--------
This module defines the database schema for the customer support platform.
Every SQLAlchemy model below maps to one SQLite table. Its columns define the
data we store, while relationships define how records connect to one another.

Relationship overview:
----------------------
Customer -> Tickets, Billing records, Conversations, Feature requests
Employee -> Assigned tickets
Product  -> Tickets, Feature requests, Known issues
Ticket   -> Conversations

How tables are created:
-----------------------
database/database.py imports Base from this file during application startup and
calls Base.metadata.create_all(). SQLAlchemy then creates any missing tables in
the configured SQLite database. Later, Alembic migrations will manage schema
changes in production.
===============================================================================
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class inherited by every SQLAlchemy model in the application."""


class Customer(Base):
    """A customer or customer organization supported by the platform."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    company: Mapped[str | None] = mapped_column(String(150))
    phone: Mapped[str | None] = mapped_column(String(50))
    country: Mapped[str | None] = mapped_column(String(100))
    timezone: Mapped[str | None] = mapped_column(String(100))
    subscription_plan: Mapped[str | None] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    registration_date: Mapped[datetime | None] = mapped_column(Date)
    renewal_date: Mapped[datetime | None] = mapped_column(Date)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    preferred_language: Mapped[str | None] = mapped_column(String(80))
    support_tier: Mapped[str | None] = mapped_column(String(80))
    account_manager: Mapped[str | None] = mapped_column(String(150))
    monthly_revenue: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    lifetime_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="customer")
    billing_records: Mapped[list["Billing"]] = relationship(back_populates="customer")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="customer")
    feature_requests: Mapped[list["FeatureRequest"]] = relationship(
        back_populates="customer"
    )
    conversation_sessions: Mapped[list["ConversationSession"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )
    memories: Mapped[list["CustomerMemory"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )


class Employee(Base):
    """A support employee who can be assigned to customer tickets."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="support_agent", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    assigned_tickets: Mapped[list["Ticket"]] = relationship(back_populates="assigned_employee")


class Product(Base):
    """A product offered or supported by the company."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    version: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="product")
    feature_requests: Mapped[list["FeatureRequest"]] = relationship(back_populates="product")
    known_issues: Mapped[list["KnownIssue"]] = relationship(back_populates="product")


class Ticket(Base):
    """A customer-support ticket created for an issue, request, or question."""

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)
    priority: Mapped[str] = mapped_column(String(30), default="medium", nullable=False)
    department: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(80))
    assigned_agent_name: Mapped[str | None] = mapped_column(String(150))
    resolution: Mapped[str | None] = mapped_column(Text)
    sentiment: Mapped[str | None] = mapped_column(String(30))
    resolution_time_hours: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    is_escalated: Mapped[bool] = mapped_column(default=False, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    assigned_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    assigned_employee: Mapped["Employee | None"] = relationship(back_populates="assigned_tickets")
    product: Mapped["Product | None"] = relationship(back_populates="tickets")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="ticket")


class Billing(Base):
    """A billing record such as an invoice, payment, or refund for a customer."""

    __tablename__ = "billing"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    invoice_number: Mapped[str | None] = mapped_column(String(100), unique=True)
    plan: Mapped[str | None] = mapped_column(String(80))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    record_type: Mapped[str] = mapped_column(String(30), default="invoice", nullable=False)
    payment_method: Mapped[str | None] = mapped_column(String(80))
    due_date: Mapped[datetime | None] = mapped_column(Date)
    paid_date: Mapped[datetime | None] = mapped_column(Date)
    refund_status: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["Customer"] = relationship(back_populates="billing_records")


class Conversation(Base):
    """One message in a customer, agent, or AI support conversation."""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    ticket_id: Mapped[int | None] = mapped_column(ForeignKey("tickets.id"))
    session_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    sender_role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["Customer"] = relationship(back_populates="conversations")
    ticket: Mapped["Ticket | None"] = relationship(back_populates="conversations")


class ConversationSession(Base):
    """One persistent support session; existing Conversation rows remain historical imported messages."""

    __tablename__ = "conversation_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    current_intent: Mapped[str | None] = mapped_column(String(80))
    current_product: Mapped[str | None] = mapped_column(String(150))
    current_issue: Mapped[str | None] = mapped_column(String(150))
    current_ticket: Mapped[str | None] = mapped_column(String(100))
    session_data: Mapped[dict | None] = mapped_column(JSON)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship(back_populates="conversation_sessions")
    messages: Mapped[list["ConversationMessage"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", order_by="ConversationMessage.created_at"
    )
    summary: Mapped["ConversationSummary | None"] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", uselist=False
    )


class ConversationMessage(Base):
    """An auditable message generated during a Phase 11 conversation session."""

    __tablename__ = "conversation_messages"
    __table_args__ = (UniqueConstraint("conversation_id", "turn_id", "role", name="uq_conversation_message_turn"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversation_sessions.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_metadata: Mapped[dict | None] = mapped_column(JSON)
    turn_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    conversation: Mapped["ConversationSession"] = relationship(back_populates="messages")


class ConversationSummary(Base):
    """Compressed working context for a long session; it never replaces original messages."""

    __tablename__ = "conversation_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversation_sessions.id"), unique=True, nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    covered_message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    conversation: Mapped["ConversationSession"] = relationship(back_populates="summary")


class CustomerMemory(Base):
    """A selectively promoted fact that is useful across a customer's future support sessions."""

    __tablename__ = "customer_memories"
    __table_args__ = (UniqueConstraint("customer_id", "memory_type", "content_normalized", name="uq_customer_memory_content"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_normalized: Mapped[str] = mapped_column(String(1_000), nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    memory_metadata: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship(back_populates="memories")


class FeatureRequest(Base):
    """A feature idea submitted by a customer for a product."""

    __tablename__ = "feature_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="submitted", nullable=False)
    priority: Mapped[str] = mapped_column(String(30), default="medium", nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["Customer"] = relationship(back_populates="feature_requests")
    product: Mapped["Product | None"] = relationship(back_populates="feature_requests")


class KnownIssue(Base):
    """A documented product problem that support agents can reference."""

    __tablename__ = "known_issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(30), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)
    workaround: Mapped[str | None] = mapped_column(Text)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    product: Mapped["Product | None"] = relationship(back_populates="known_issues")
