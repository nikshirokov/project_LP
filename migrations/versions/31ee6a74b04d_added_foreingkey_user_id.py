"""added foreingkey user_id

Revision ID: 31ee6a74b04d
Revises: 649762b05dd7
Create Date: 2024-01-29 20:05:57.928626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31ee6a74b04d'
down_revision = '649762b05dd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_constraint('fk_article_user_id_user', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_article_user_id_user'), 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_article_user_id_user'), type_='foreignkey')
        batch_op.create_foreign_key('fk_article_user_id_user', 'user', ['user_id'], ['username'])

    # ### end Alembic commands ###
