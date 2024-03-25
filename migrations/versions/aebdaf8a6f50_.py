"""empty message

Revision ID: aebdaf8a6f50
Revises: a4237dc1d1c3
Create Date: 2024-03-25 13:19:37.228763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aebdaf8a6f50'
down_revision = 'a4237dc1d1c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('access_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('email_address', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='login_pkey')
    )
    # ### end Alembic commands ###
