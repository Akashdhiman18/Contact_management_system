"""empty message

Revision ID: a4237dc1d1c3
Revises: 2ebf052e8119
Create Date: 2024-03-22 03:16:39.585165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4237dc1d1c3'
down_revision = '2ebf052e8119'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registeruser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('emailaddress', sa.String(length=500), nullable=True),
    sa.Column('passcode', sa.String(length=500), nullable=True),
    sa.Column('mobileno', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registeruser')
    # ### end Alembic commands ###