""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from flask import redirect, render_template, url_for, flash
from flask_login import login_required

from app import db

from ..models.car_bay import CarBay
from ..models.parking_lot import ParkingLot
from . import bookings


@bookings.route("/parking-lots")
@login_required
def parking_lots():
    """ route to select a parking lot to view bay availabilties for """
    parking_lots = ParkingLot.query.all()
    return render_template("bookings/parking_lots.html", parking_lots=parking_lots)


@bookings.route("/bays/<int:lot_number>/")
@login_required
def bays(lot_number):
    """ route to view availabilities of bays in parking lot with lot number """
    lot = ParkingLot.query.filter_by(lot_number=lot_number).first()

    if lot is None:
        flash("Something went wrong: bays for this parking lot could not be found.")
        return redirect(url_for("bookings.parking_lots"))

    return render_template("bookings/bays.html", lot=lot, bays=lot.bays)
