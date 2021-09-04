""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from datetime import date

from flask import render_template, redirect, flash, url_for
from flask_login import login_required

from . import bookings
from .helpers import get_lot_bookings, get_times, get_date, get_bay_bookings


@bookings.route("/parking-lots/<int:day>/<int:month>/<int:year>")
@bookings.route("/parking-lots/today")
@login_required
def parking_lots(day=date.today().day, month=date.today().month, year=date.today().year):
    """ route to select a parking lot to view bay availabilties for """

    view_date = get_date(day, month, year)
    if view_date is None:
        return redirect(url_for("admin.parking_lots"))

    all_lots, bookings = get_lot_bookings(view_date)

    times = get_times()

    return render_template(
        "bookings/parking_lots.html",
        parking_lots=all_lots,
        bookings=bookings,
        times=times,
        view_date=view_date,
    )


@bookings.route("/bay/<int:bay_id>/today")
@bookings.route("/bay/<int:bay_id>/<int:day>/<int:month>/<int:year>")
@login_required
def bay(bay_id, day=date.today().day, month=date.today().month, year=date.today().year):
    """ route to view a bays availability for the week """

    view_date = get_date(day, month, year)
    if view_date is None:
        return redirect(url_for("admin.bays"))

    bay, availabilities, end_date = get_bay_bookings(bay_id, view_date)

    if not (bay and availabilities and end_date):
        flash("Something went wrong could not find the bay.")
        return redirect(url_for("bookings.parking_lots"))

    times = get_times()

    print(availabilities)

    return render_template(
        "bookings/bay.html",
        bay=bay,
        availabilities=availabilities,
        times=times,
        start_date=view_date,
        end_date=end_date
    )