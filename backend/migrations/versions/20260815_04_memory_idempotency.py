"""Enforce Phase 11 turn and durable-memory idempotency at the database layer."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260815_04"
down_revision: str | None = "20260815_03"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """Prevent retry-created duplicate messages and concurrent duplicate customer memories."""
    with op.batch_alter_table("conversation_messages") as batch_op:
        batch_op.add_column(sa.Column("turn_id", sa.String(length=64), nullable=True))
        batch_op.create_unique_constraint("uq_conversation_message_turn", ["conversation_id", "turn_id", "role"])
    with op.batch_alter_table("customer_memories") as batch_op:
        batch_op.add_column(sa.Column("content_normalized", sa.String(length=1000), nullable=True))
    op.execute("UPDATE customer_memories SET content_normalized = lower(trim(content))")
    with op.batch_alter_table("customer_memories") as batch_op:
        batch_op.alter_column("content_normalized", nullable=False)
        batch_op.create_unique_constraint(
            "uq_customer_memory_content", ["customer_id", "memory_type", "content_normalized"]
        )


def downgrade() -> None:
    """Remove only idempotency constraints and columns introduced by this migration."""
    with op.batch_alter_table("customer_memories") as batch_op:
        batch_op.drop_constraint("uq_customer_memory_content", type_="unique")
        batch_op.drop_column("content_normalized")
    with op.batch_alter_table("conversation_messages") as batch_op:
        batch_op.drop_constraint("uq_conversation_message_turn", type_="unique")
        batch_op.drop_column("turn_id")
