"""add foreign key to the posts table

Revision ID: 644911243b4f
Revises: 0a08a1abc55b
Create Date: 2024-07-29 12:12:57.559050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '644911243b4f'
down_revision: Union[str, None] = '0a08a1abc55b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: 
    op.add_column("posts",sa.Column("user_id",sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
    local_cols=['user_id'],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
