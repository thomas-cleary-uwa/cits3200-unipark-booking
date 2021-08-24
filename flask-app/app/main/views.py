""" Routes used by main blueprint

Authors: Thomas Cleary,
"""

from app import db
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from ..models.parking_lot import ParkingLot
from ..models.car_bay import CarBay
from . import main


@main.route('/')
@main.route('/index')
@login_required
def index():
    """ Initial route for the application. """
    parking_lots = ParkingLot.query.all()

    if current_user.is_administrator():
        return redirect(url_for("admin.index"))
    return render_template('main/index.html', lots=parking_lots)
