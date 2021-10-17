"""make contact number nullable

Revision ID: 7e8d11419758
Revises: 30366f8d2c42
Create Date: 2021-10-17 11:06:05.257684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e8d11419758'
down_revision = '30366f8d2c42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index('ix_User_contact_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index('ix_User_contact_number', ['contact_number'], unique=False)

    # ### end Alembic commands ###
