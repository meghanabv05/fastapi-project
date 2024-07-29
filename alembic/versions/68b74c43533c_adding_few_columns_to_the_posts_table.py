"""adding few columns to the posts table

Revision ID: 68b74c43533c
Revises: 644911243b4f
Create Date: 2024-07-29 12:29:36.494623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68b74c43533c'
down_revision: Union[str, None] = '644911243b4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="True", nullable=False),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),)

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
 