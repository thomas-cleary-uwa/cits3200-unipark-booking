""" Initialise the bookings blueprint of the application

Authors: Thomas Cleary,
"""

from flask import Blueprint

bookings = Blueprint('bookings', __name__)

from . import routes, forms