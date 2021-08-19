""" Routes used by main blueprint

Authors: Thomas Cleary,
"""

from app import db
from flask import render_template

from ..models.parking_lot import ParkingLot
from ..models.car_bay import CarBay
from . import main


@main.route('/')
@main.route('/index')
def index():
    """ Initial route for the application. """
    parking_lots = ParkingLot.query.all()

    return render_template('main/index.html', title='index', lots=parking_lots)
