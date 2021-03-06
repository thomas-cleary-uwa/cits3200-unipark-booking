"""add booking model

Revision ID: c47c453f45b1
Revises: af49ff71cfc3
Create Date: 2021-09-02 22:52:43.949015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c47c453f45b1'
down_revision = 'af49ff71cfc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_code', sa.String(length=16), nullable=False),
    sa.Column('datetime_placed', sa.DateTime(), nullable=False),
    sa.Column('date_booked', sa.Date(), nullable=False),
    sa.Column('timeslot_start', sa.Integer(), nullable=False),
    sa.Column('timeslot_end', sa.Integer(), nullable=False),
    sa.Column('guest_name', sa.String(length=64), nullable=False),
    sa.Column('vehicle_rego', sa.String(length=16), nullable=True),
    sa.Column('bay_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bay_id'], ['CarBay.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bay_id', 'date_booked', 'timeslot_start', 'timeslot_end'),
    sa.UniqueConstraint('booking_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Booking')
    # ### end Alembic commands ###
