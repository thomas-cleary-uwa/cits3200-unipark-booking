""" Helper functions for the routes in the Bookings blueprint

Authors: Thomas Cleary,
"""

from datetime import date

from app import db

from ..models.parking_lot import ParkingLot
from ..models.car_bay     import CarBay
from ..models.booking     import Booking


def get_lot_bookings(parking_lots, date_obj):
    """ return a dict with {parkinglot : {carbay : [1,2,3]}}

    a dict of dicts, one for each parking lot and one for each bay in the lot,
    the value of the bay key is the timeslots that are booked for the given day
    """

    bookings = {lot.lot_number : {bay.bay_number : [False] * 32 for bay in lot.bays} for lot in parking_lots}
    
    for lot in parking_lots:
        for bay in lot.bays:
            # get bookings
            today_bookings = Booking.query.filter_by(
                date_booked=date_obj, bay_id=bay.id).all()

            for booking in today_bookings:
                for timeslot in range(booking.timeslot_start, booking.timeslot_end+1):
                    bookings[lot.lot_number][bay.bay_number][timeslot-1] = True

    return bookings

