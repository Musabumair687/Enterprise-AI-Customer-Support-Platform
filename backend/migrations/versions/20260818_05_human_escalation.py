"""Add Phase 13 ticket handoff fields and supported workflow states."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260818_05"
down_revision: str | None = "20260815_04"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.add_column(sa.Column("escalation_reason", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.drop_column("resolved_at")
        batch_op.drop_column("escalation_reason")
