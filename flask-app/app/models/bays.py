""" Models that relate to car bays that are managed by the application

Authors: Thomas Cleary,
"""

from .. import db


class ParkingLot(db.Model):
    """ Represents a parking lot that can contain multiple car bays """             
    __tablename__ = "ParkingLot"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    lot_number = db.Column(db.Integer, unique=True, nullable=False)
    # location?

    # Relationships


    def __repr__(self):
        return "<Parking Lot {}".format(self.lot_number)



class Bay(db.Model):
    """ Represents a car bay.

    That can be reserved by a UWA staff member for guests.
    """