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

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
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
