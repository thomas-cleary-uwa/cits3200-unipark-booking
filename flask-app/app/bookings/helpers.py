""" Helper functions for the routes in the Bookings blueprint

Authors: Thomas Cleary,
"""

import random
import pdfkit

from datetime import date, datetime, timedelta
from hashlib import md5
from threading import Thread

from flask import flash, render_template, url_for, current_app
from flask_login import current_user
from sqlalchemy import and_

from app import db

from ..models.parking_lot import ParkingLot
from ..models.car_bay     import CarBay
from ..models.booking     import Booking
from ..models.user        import User

from ..helpers.email import send_email


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


def get_date(day, month, year):
    try:
        return date(year, month, day)
    except ValueError:
        flash("Invalid Date Requested")
        return None


def get_bay_bookings(bay_id, view_date):
    """ return bay, a dict of bay availabilities for the week, end date

    availabilities {day : [TRUE/FALSE] * 32}
    """
    bay = CarBay.query.get(bay_id)
    if bay is None:
        return (False, False, False)
    
    dates = [view_date + timedelta(days=x) for x in range(0, 7)]

    bookings = Booking.query. \
        filter_by(bay_id=bay.id). \
        filter(and_(dates[0] <= Booking.date_booked, Booking.date_booked <= dates[-1]))
   
    availabilities  = {date : [False] * 32 for date in dates}

    for booking in bookings:
        for timeslot in range(booking.timeslot_start, booking.timeslot_end+1):
            availabilities[booking.date_booked][timeslot-1] = True  

    return (bay, availabilities, dates[-1])


def is_valid_bay(lot_num, bay_num):
    lot = ParkingLot.query.filter_by(lot_number=lot_num).first()
    bay = CarBay.query.filter_by(bay_number=bay_num, parking_lot_id=lot.id).first()

    if lot is None or bay is None:
        return (False, None)
    
    return (True, bay)


def is_valid_date(day, month, year):
    try:
        return (True, date(year, month, day))
    except ValueError:
        return (False, None)


def attempt_booking(form, bay, date, start, end):
    # get all bookings for the bay with bay_num in lot with lot_num on date
    current_bookings = Booking.query.filter_by(
        date_booked=date, bay_id=bay.id
    ).all()

    booked_times = set()

    for booking in current_bookings:
        times_booked = list(range(booking.timeslot_start, booking.timeslot_end+1))

        for time in times_booked:
            booked_times.add(time)

    # check if new booking overlaps with previously made bookings
    new_booking_times = range(start, end+1)

    if start in booked_times or end in booked_times:
        return False

    for time in new_booking_times:
        if time in booked_times:
            return False

    # if we didnt find an overlap, add this new booking to the db
    time_placed = datetime.now()

    booking_code = md5((str(time_placed) + current_user.email + str(random.randint(1, 10))).encode()). \
                        hexdigest()[:10]

    guest_name = "{} {} {}".format(
        form.title.data,
        form.guest_first_name.data.strip().capitalize(),
        form.guest_last_name.data.strip().capitalize()
    )

    vehicle_rego = form.vehicle_rego.data.strip().upper()

    times = get_times(num_slots=33)
    start_time = times[start-1]
    end_time   = times[end]


    new_booking = Booking(
        booking_code    = booking_code,
        datetime_placed = time_placed,
        date_booked     = date,
        timeslot_start  = start,
        timeslot_end    = end,
        start_time      = start_time,
        end_time        = end_time,
        guest_name      = guest_name,
        vehicle_rego    = vehicle_rego,
        bay_id          = bay.id,
        user_id         = current_user.id
    )

    db.session.add(new_booking)
    db.session.commit()

    # use seperate thread to generate pdf

    bay = new_booking.bay

    lot_num = bay.lot.lot_number
    bay_num = bay.bay_number
    
    thr = Thread(target=generate_reservation_sign, args=[
        current_app._get_current_object(),
        new_booking,
        bay_num,
        lot_num,
        User.query.get(current_user.id)
    ])
    thr.start()

    return True


def generate_reservation_sign(app, booking, bay_num, lot_num, user):
    with app.app_context():
        html = render_template(
            "pdf/reservation_sign.html",
            booking=booking,
            bay_num=bay_num,
            lot_num=lot_num
        )

        options = {
            "--orientation" : "landscape",
            "--margin-bottom" : 20,
            "--margin-left" : 25,
            "--margin-right" : 30,
            "--margin-top" : 20
        }

        pdfkit.from_string(
            html,
            "./app/static/reservation_signs/{}.pdf".format(booking.booking_code),
            css="./app/static/css/reservation_sign.css",
            options=options
        )

        attachments = {
            "application/pdf" : [
                "static/reservation_signs/{}.pdf".format(booking.booking_code)
            ]
        }

        send_email(
            user.email,
            'Booking Confirmed',
            'email/confirm_booking',
            booking=booking,
            lot_num=lot_num,
            bay_num=bay_num,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
            attachments=attachments
    )



    