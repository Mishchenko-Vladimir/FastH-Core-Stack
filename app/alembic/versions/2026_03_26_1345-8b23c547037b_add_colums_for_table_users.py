"""add colums for table users

Revision ID: 8b23c547037b
Revises: 5ae2cd33ec7e
Create Date: 2026-03-26 13:45:12.454622

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8b23c547037b"
down_revision: Union[str, Sequence[str], None] = "5ae2cd33ec7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
    )
    op.create_index(
        op.f("ix_users_created_at"),
        "users",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_column("users", "created_at")
