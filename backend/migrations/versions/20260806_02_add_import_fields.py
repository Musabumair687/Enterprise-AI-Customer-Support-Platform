"""Add source-data fields required by the CSV import scripts.

Revision ID: 20260806_02
Revises: 20260806_01
Create Date: 2026-08-06

External source IDs make imports idempotent: rerunning a CSV importer can skip
records that already exist instead of inserting duplicates.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260806_02"
down_revision: str | None = "20260806_01"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """Add customer, ticket, and billing fields represented in the CSV files."""
    with op.batch_alter_table("customers") as batch_op:
        batch_op.add_column(sa.Column("external_id", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("country", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("timezone", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("subscription_plan", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("registration_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("renewal_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("last_login", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("preferred_language", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("support_tier", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("account_manager", sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column("monthly_revenue", sa.Numeric(precision=12, scale=2), nullable=True))
        batch_op.add_column(sa.Column("lifetime_value", sa.Numeric(precision=14, scale=2), nullable=True))
        batch_op.create_index("ix_customers_external_id", ["external_id"], unique=True)

    with op.batch_alter_table("tickets") as batch_op:
        batch_op.add_column(sa.Column("external_id", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("department", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("assigned_agent_name", sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column("resolution", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("sentiment", sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column("resolution_time_hours", sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column("is_escalated", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch_op.create_index("ix_tickets_external_id", ["external_id"], unique=True)

    with op.batch_alter_table("billing") as batch_op:
        batch_op.add_column(sa.Column("plan", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("payment_method", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("due_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("paid_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("refund_status", sa.String(length=50), nullable=True))


def downgrade() -> None:
    """Remove source-data fields added for CSV imports."""
    with op.batch_alter_table("billing") as batch_op:
        batch_op.drop_column("refund_status")
        batch_op.drop_column("paid_date")
        batch_op.drop_column("due_date")
        batch_op.drop_column("payment_method")
        batch_op.drop_column("plan")

    with op.batch_alter_table("tickets") as batch_op:
        batch_op.drop_index("ix_tickets_external_id")
        batch_op.drop_column("is_escalated")
        batch_op.drop_column("resolution_time_hours")
        batch_op.drop_column("sentiment")
        batch_op.drop_column("resolution")
        batch_op.drop_column("assigned_agent_name")
        batch_op.drop_column("department")
        batch_op.drop_column("external_id")

    with op.batch_alter_table("customers") as batch_op:
        batch_op.drop_index("ix_customers_external_id")
        batch_op.drop_column("lifetime_value")
        batch_op.drop_column("monthly_revenue")
        batch_op.drop_column("account_manager")
        batch_op.drop_column("support_tier")
        batch_op.drop_column("preferred_language")
        batch_op.drop_column("last_login")
        batch_op.drop_column("renewal_date")
        batch_op.drop_column("registration_date")
        batch_op.drop_column("subscription_plan")
        batch_op.drop_column("timezone")
        batch_op.drop_column("country")
        batch_op.drop_column("external_id")
