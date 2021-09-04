""" Helper functions for the routes in the Bookings blueprint

Authors: Thomas Cleary,
"""

from ..models.parking_lot import ParkingLot
from ..models.booking     import Booking


def get_lot_bookings(date_obj):
    """ return a dict with {parkinglot : {carbay : [1,2,3]}}

    a dict of dicts, one for each parking lot and one for each bay in the lot,
    the value of the bay key is the timeslots that are booked for the given day
    """
    parking_lots = ParkingLot.query.all()

    bookings = {lot.lot_number : {bay.bay_number : [False] * 32 for bay in lot.bays} for lot in parking_lots}
    
    for lot in parking_lots:
        for bay in lot.bays:
            # get bookings
            today_bookings = Booking.query.filter_by(
                date_booked=date_obj, bay_id=bay.id).all()

            for booking in today_bookings:
                for timeslot in range(booking.timeslot_start, booking.timeslot_end+1):
                    bookings[lot.lot_number][bay.bay_number][timeslot-1] = True

    return (parking_lots, bookings)


def get_times(num_slots=32):
    """ return a list of times from 9am-5pm divided by num_slots """
    hour = 9
    minutes = 0

    times = []

    for i in range(num_slots):
        if minutes == 0:
            minutes = "00"
        time = str(hour) + ":" + str(minutes)
        if hour < 12:
            time += " AM"
        else:
            time += " PM"

        minutes = int(minutes)

        minutes += 15
        if minutes == 60:
            minutes = 0
            hour += 1

        times.append(time)

    return times
