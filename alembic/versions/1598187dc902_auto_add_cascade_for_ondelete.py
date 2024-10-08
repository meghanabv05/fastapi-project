"""auto-add_cascade_for_ondelete

Revision ID: 1598187dc902
Revises: c3966c163913
Create Date: 2024-07-29 12:59:36.970692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1598187dc902'
down_revision: Union[str, None] = 'c3966c163913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('votes_user_id_fkey', 'votes', type_='foreignkey')
    op.drop_constraint('votes_post_id_fkey', 'votes', type_='foreignkey')
    op.create_foreign_key(None, 'votes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'votes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.create_foreign_key('votes_post_id_fkey', 'votes', 'posts', ['post_id'], ['id'])
    op.create_foreign_key('votes_user_id_fkey', 'votes', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
