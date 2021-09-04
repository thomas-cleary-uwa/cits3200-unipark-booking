""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from datetime import date

from flask import redirect, render_template, url_for, flash
from flask_login import login_required

from app import db

from ..models.car_bay import CarBay
from ..models.parking_lot import ParkingLot
from . import bookings
from .route_helpers import get_lot_bookings, get_times


@bookings.route("/parking-lots/<int:day>/<int:month>/<int:year>")
@bookings.route("/parking-lots")
@login_required
def parking_lots(day=date.today().day, month=date.today().month, year=date.today().year):
    """ route to select a parking lot to view bay availabilties for """
    parking_lots = ParkingLot.query.all()

    bookings = get_lot_bookings(parking_lots, date(year, month, day))

    times = get_times()

    view_date = date(year, month, day)

    return render_template(
        "bookings/parking_lots.html",
        parking_lots=parking_lots,
        bookings=bookings,
        times=times,
        view_date=view_date,
    )


@bookings.route("/bays/<int:lot_number>/")
@login_required
def bays(lot_number):
    """ route to view availabilities of bays in parking lot with lot number """
    lot = ParkingLot.query.filter_by(lot_number=lot_number).first()

    if lot is None:
        flash("Something went wrong: bays for this parking lot could not be found.")
        return redirect(url_for("bookings.parking_lots"))

    return render_template("bookings/bays.html", lot=lot, bays=lot.bays)
