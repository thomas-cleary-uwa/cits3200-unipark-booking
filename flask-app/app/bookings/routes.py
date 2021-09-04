""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from datetime import date

from flask import render_template
from flask_login import login_required

from . import bookings
from .helpers import get_lot_bookings, get_times


@bookings.route("/parking-lots/<int:day>/<int:month>/<int:year>")
@bookings.route("/parking-lots/today")
@login_required
def parking_lots(day=date.today().day, month=date.today().month, year=date.today().year):
    """ route to select a parking lot to view bay availabilties for """
    parking_lots, bookings = get_lot_bookings(date(year, month, day))

    times = get_times()

    view_date = date(year, month, day)

    return render_template(
        "bookings/parking_lots.html",
        parking_lots=parking_lots,
        bookings=bookings,
        times=times,
        view_date=view_date,
    )
