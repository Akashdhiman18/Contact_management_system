"""empty message

Revision ID: aaa00da074ea
Revises: 
Create Date: 2024-03-26 13:16:00.218451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaa00da074ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=1000), nullable=True),
    sa.Column('last_name', sa.String(length=1000), nullable=True),
    sa.Column('email_address', sa.String(length=500), nullable=True),
    sa.Column('mobile', sa.String(length=30), nullable=True),
    sa.Column('home_address', sa.String(length=1000), nullable=True),
    sa.Column('url_of_picture', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('contact_id')
    )
    op.create_table('systemuser',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('email_address', sa.String(length=500), nullable=True),
    sa.Column('passcode', sa.String(length=500), nullable=True),
    sa.Column('mobile_no', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('systemuser')
    op.drop_table('contacts')
    # ### end Alembic commands ###