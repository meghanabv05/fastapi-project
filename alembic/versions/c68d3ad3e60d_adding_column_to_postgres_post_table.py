"""adding column to postgres post table

Revision ID: c68d3ad3e60d
Revises: b1249d47b827
Create Date: 2024-07-29 11:34:16.146869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c68d3ad3e60d'
down_revision: Union[str, None] = 'b1249d47b827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
 