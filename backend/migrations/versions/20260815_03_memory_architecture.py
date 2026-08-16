"""Create persistent session, message, summary, and selective customer-memory storage for Phase 11."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260815_03"
down_revision: str | None = "20260806_02"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """Add Phase 11 tables without changing existing imported conversation history."""
    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id"), nullable=False),
        sa.Column("session_id", sa.String(length=100), nullable=False, unique=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("current_intent", sa.String(length=80)),
        sa.Column("current_product", sa.String(length=150)),
        sa.Column("current_issue", sa.String(length=150)),
        sa.Column("current_ticket", sa.String(length=100)),
        sa.Column("session_data", sa.JSON()),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_conversation_sessions_customer_id", "conversation_sessions", ["customer_id"])
    op.create_index("ix_conversation_sessions_session_id", "conversation_sessions", ["session_id"], unique=True)
    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversation_sessions.id"), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("message_metadata", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_conversation_messages_conversation_id", "conversation_messages", ["conversation_id"])
    op.create_index("ix_conversation_messages_created_at", "conversation_messages", ["created_at"])
    op.create_table(
        "conversation_summaries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversation_sessions.id"), nullable=False, unique=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("covered_message_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_conversation_summaries_conversation_id", "conversation_summaries", ["conversation_id"], unique=True)
    op.create_table(
        "customer_memories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id"), nullable=False),
        sa.Column("memory_type", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("importance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("memory_metadata", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_customer_memories_customer_id", "customer_memories", ["customer_id"])
    op.create_index("ix_customer_memories_memory_type", "customer_memories", ["memory_type"])


def downgrade() -> None:
    """Remove only Phase 11 tables; existing conversations remain untouched."""
    op.drop_table("customer_memories")
    op.drop_table("conversation_summaries")
    op.drop_table("conversation_messages")
    op.drop_table("conversation_sessions")
