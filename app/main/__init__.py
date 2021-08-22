""" Initialise the main blueprint of the application

Authors: Thomas Cleary,
"""

from flask import Blueprint

main = Blueprint('main', __name__)

# avoid circular imports (both modules import main blueprint)
from . import views, errors
# from ..models.user import Permission (will we have user permissions?)
