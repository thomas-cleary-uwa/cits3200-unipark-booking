""" Routes associated with making a booking

Authors: Thomas Cleary,
"""

from datetime import date, timedelta

from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import login_required, current_user

from . import bookings
from .forms import ConfirmBookingForm
from .helpers import (
    get_lot_bookings, get_times, get_date, get_bay_bookings,
    is_valid_bay, is_valid_date, attempt_booking, get_user_bookings,
    check_user, delete_booking 
)  

##############################################################################
# New Booking Routes #########################################################
##############################################################################
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

    except ValueError as error:
        flash("Booking failed. Invalid booking request.")
        return redirect(url_for("bookings.parking_lots"))
    except KeyError as error:
        flash("Invalid booking url.")
        return redirect(url_for("bookings.parking_lot"))

    
    # for setting up fresh app and adding in fake bookings
    try:
        no_email = bool(request.args['no_email'])
    except (KeyError, ValueError) as error:
        no_email = False

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

        booked = attempt_booking(confirm_form, bay, booking_date, start, end, no_email)

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
        

##############################################################################
# Manage Bookings Routes #####################################################
##############################################################################

@bookings.route("manage")
@login_required
def manage():
    """ route for user to manage their bookings (all users if admin) """
    # all users if admin, else just current user's bookings
    user_bookings, users = get_user_bookings(current_user)

    if len(user_bookings.keys()) == 0:
        user_bookings = None

    return render_template("bookings/manage.html", bookings=user_bookings, users=users)


@bookings.route("delete/<booking_code>")
@login_required
def delete(booking_code):
    # check that booking code matches current user or user is admin
    valid_delete = check_user(booking_code)

    if not valid_delete:
        flash("You do not have permission to delete this booking")

    else:
        booking_deleted = delete_booking(booking_code)

        if not booking_deleted:
            flash("Something went wrong: Unable to delete booking")
        else:
            flash("Booking Deleted Successfully")

    return redirect(url_for("bookings.manage"))


@bookings.route("reservation-sign/<booking_code>")
@login_required
def reservation_sign(booking_code):
    valid_booking = check_user(booking_code, check_sign=True)
    if not valid_booking:
        flash("Cannot find reservation sign for this booking")
        return redirect(url_for("bookings.manage"))
    
    return current_app.send_static_file("reservation_signs/{}.pdf".format(booking_code))
