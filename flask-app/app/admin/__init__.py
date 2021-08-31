""" Initialise the admin blueprint of the application

Authors: Thomas Cleary,
"""

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views, forms