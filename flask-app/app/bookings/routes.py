""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from datetime import date, timedelta

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required

from . import bookings
from .forms import ConfirmBookingForm
from .helpers import (
    get_lot_bookings, get_times, get_date, get_bay_bookings,
    is_valid_bay, is_valid_date, attempt_booking
) 


@bookings.route("/parking-lots/<int:day>/<int:month>/<int:year>")
@bookings.route("/parking-lots/today")
@login_required
def parking_lots(day=date.today().day, month=date.today().month, year=date.today().year):
    """ route to select a parking lot to view bay availabilties for """

    view_date = get_date(day, month, year)
    if view_date is None:
        return redirect(url_for("admin.parking_lots"))

    all_lots, lot_bookings = get_lot_bookings(view_date)

    times = get_times()

    return render_template(
        "bookings/parking_lots.html",
        parking_lots=all_lots,
        bookings=lot_bookings,
        times=times,
        view_date=view_date,
    )


@bookings.route("/parking-lots/next/<direction>/<int:day>/<int:month>/<int:year>")
@login_required
def parking_lots_next(direction, day, month, year):
    direction = int(direction)
    next_date = date(year, month, day) + timedelta(days=direction)

    if next_date < date.today():
        next_date = date.today()
        flash("Cannot view historical availabilities")

    return redirect(url_for("bookings.parking_lots",
        day=next_date.day,
        month=next_date.month,
        year=next_date.year
    ))


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

    return render_template(
        "bookings/bay.html",
        bay=bay,
        availabilities=availabilities,
        times=times,
        start_date=view_date,
        end_date=end_date
    )


@bookings.route("/bay/<int:bay_id>/next/<direction>/<int:day>/<int:month>/<int:year>")
@login_required
def bay_next(direction, bay_id, day, month, year):
    direction = int(direction)

    next_date = date(year, month, day) + timedelta(days=direction * 7)
    if next_date < date.today():
        next_date = date.today()
        flash("Cannot view historical availabilities")

    return redirect(url_for("bookings.bay",
        bay_id=bay_id,
        day=next_date.day,
        month=next_date.month,
        year=next_date.year
    ))


# this is really long
# if we implement this as an api endpoint using Javascript requests we do not need such a long URI
@bookings.route("/confirm", methods=['GET', 'POST'])
@login_required
def confirm_booking():
    confirm_form = ConfirmBookingForm()

    try:
        lot_num = int(request.args['lot_num'])
        bay_num = int(request.args['bay_num'])
        day     = int(request.args['day'])
        month   = int(request.args['month'])
        year    = int(request.args['year'])
        start   = int(request.args['start'])
        end     = int(request.args['end'])

    except ValueError:
        flash("Booking failed. Invalid booking request.")
        return redirect(url_for("bookings.parking_lots"))

    valid_bay, bay = is_valid_bay(lot_num, bay_num)
    if not valid_bay:
        flash("Booking failed. Bay is invalid.")
        return redirect(url_for("bookings.parking_lots"))

    valid_date, booking_date = is_valid_date(day, month, year)
    if not valid_date:
        flash("Booking failed. Date invalid.")
        return redirect(url_for("bookings.parking_lots"))

    if confirm_form.validate_on_submit():
        if not confirm_form.ts_and_cs.data:
            flash("You need to accept the terms and conditions")
            return redirect(url_for(
                "bookings.confirm_booking",
                lot_num=lot_num, bay_num=bay_num,
                day=day, month=month, year=year, 
                start=start, end=end
            ))

        booked = attempt_booking(confirm_form, bay, booking_date, start, end)

        if not booked: 
            flash("Booking failed. Invalid booking times")
        else:
            flash("Booking succeeded")

        return redirect(url_for("bookings.parking_lots"))

    times = get_times(num_slots=33)
    start_time = times[start-1]
    end_time   = times[end]

    return render_template("bookings/confirm_booking.html", 
        form=confirm_form,
        date=booking_date,
        lot_num=lot_num,
        bay_num=bay_num,
        start=start,
        start_time=start_time,
        end=end,
        end_time=end_time
    )

    
        
        

        