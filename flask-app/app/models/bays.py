""" Models that relate to car bays that are managed by the application

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
    car_bays = db.relationship('CarBay', backref="parking_lot")


    def __repr__(self):
        return "<Parking Lot {}>".format(self.lot_number)



class CarBay(db.Model):
    """ Represents a car bay.

    That can be reserved by a UWA staff member for guests.
    """
    __tablename__ = "CarBay"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    bay_number = db.Column(db.Integer, nullable=False)
    # location?

    # Foreign Keys
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('ParkingLot.id'))

    # Relationships


    def __repr__(self):
        return "<Car Bay {} in Lot {}>".format(
            self.bay_number, self.parking_lot.lot_number
        )
