"""add openrouter settings

Revision ID: 002
Revises: 001
Create Date: 2026-05-15 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("settings", sa.Column("openrouter_api_key", sa.String(512), nullable=True))
    op.add_column(
        "settings",
        sa.Column("openrouter_model", sa.String(255), nullable=False, server_default="openai/gpt-4o-mini"),
    )
    op.add_column(
        "settings",
        sa.Column(
            "openrouter_system_prompt",
            sa.Text(),
            nullable=False,
            server_default="You are a helpful Telegram support assistant. Reply clearly and concisely.",
        ),
    )
    op.add_column(
        "settings",
        sa.Column("openrouter_history_limit", sa.Integer(), nullable=False, server_default="10"),
    )
    op.add_column(
        "settings",
        sa.Column("ai_auto_reply_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("settings", "ai_auto_reply_enabled")
    op.drop_column("settings", "openrouter_history_limit")
    op.drop_column("settings", "openrouter_system_prompt")
    op.drop_column("settings", "openrouter_model")
    op.drop_column("settings", "openrouter_api_key")
