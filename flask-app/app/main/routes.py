""" Routes used by main blueprint

Authors: Thomas Cleary,
"""

from datetime import date

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main


@main.route('/')
@main.route('/index')
@login_required
def index():
    """ Initial route for the application. """
    if current_user.is_administrator():
        return redirect(url_for("admin.index"))

    today = date.today()
    return redirect(
        url_for(
            "bookings.parking_lots",
            year=today.year, 
            month=today.month,
            day=today.day
        ))
