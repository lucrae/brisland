"""empty message

Revision ID: 06765e57aee1
Revises: 
Create Date: 2018-06-25 20:17:52.886864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06765e57aee1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###