""" Models that relate to a booking, 

Authors: Thomas Cleary, 
"""

from datetime import datetime, date

from .. import db


class Booking(db.Model):
    """ Represents a Booking made by a User """
    __tablename__ = "Booking"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    booking_code    = db.Column(db.String(16), unique=True, nullable=False)
    datetime_placed = db.Column(db.DateTime, nullable=False, default=datetime.now)

    date_booked     = db.Column(db.Date, nullable=False)
    timeslot_start  = db.Column(db.Integer, nullable=False)
    timeslot_end    = db.Column(db.Integer, nullable=False)

    guest_name      = db.Column(db.String(64), nullable=False)
    vehicle_rego    = db.Column(db.String(16), nullable=True)

    # Foregn Keys
    bay_id          = db.Column(db.Integer, db.ForeignKey('CarBay.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('User.id'))

    # Constraints
    db.UniqueConstraint(bay_id, date_booked, timeslot_start, timeslot_end)
