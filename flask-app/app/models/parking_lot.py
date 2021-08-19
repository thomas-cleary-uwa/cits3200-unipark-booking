""" Models that relate to parking lots that are managed by the application

Authors: Thomas Cleary,
"""

from .. import db


class ParkingLot(db.Model):
    """ Represents a Parking Lot

    That can contain multiple '30 mins unless reserved' car bays.
    """
    __tablename__ = "ParkingLot"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    lot_number = db.Column(db.Integer, unique=True, nullable=False)
    # location?

    # Relationships
    bays = db.relationship('CarBay', backref="lot")


    def __repr__(self):
        return "<Parking Lot {}>".format(self.lot_number)
