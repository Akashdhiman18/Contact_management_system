"""empty message

Revision ID: 1cd2faf301f4
Revises: fc386418b83f
Create Date: 2024-03-25 13:44:05.083846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cd2faf301f4'
down_revision = 'fc386418b83f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=1000), nullable=True),
    sa.Column('last_name', sa.String(length=1000), nullable=True),
    sa.Column('email_address', sa.String(length=500), nullable=True),
    sa.Column('mobile', sa.String(length=30), nullable=True),
    sa.Column('home_address', sa.String(length=1000), nullable=True),
    sa.Column('url_of_picture', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('systemuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('emailaddress', sa.String(length=500), nullable=True),
    sa.Column('passcode', sa.String(length=500), nullable=True),
    sa.Column('mobileno', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    op.drop_table('registeruser')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registeruser',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('emailaddress', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('passcode', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('mobileno', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='registeruser_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('email_address', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('mobile', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('home_address', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('url_of_picture', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.drop_table('systemuser')
    op.drop_table('contacts')
    # ### end Alembic commands ###