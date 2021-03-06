""" Models that relate to car bays that are managed by the application

Authors: Thomas Cleary,
"""

from .. import db


class CarBay(db.Model):
    """ Represents a car bay.

    That can be reserved by a UWA staff member for guests.
    """
    __tablename__ = "CarBay"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    bay_number = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Constraints
    db.UniqueConstraint(latitude, longitude)

    # Foreign Keys
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('ParkingLot.id'))

    # Relationships
    bookings = db.relationship('Booking', backref="bay", lazy="dynamic")


    def __repr__(self):
        return "<Car Bay {} in Lot {}>".format(
            self.bay_number, self.lot.lot_number
        )