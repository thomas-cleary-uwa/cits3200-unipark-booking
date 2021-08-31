""" Initialise the auth blueprint of the application

Authors: Thomas Cleary,
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, forms