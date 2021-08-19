""" Defines Flask App Instance.

Defines the Flask application instance and some tasks to help manage it.
This file will be executed when the 'flask run' command is used.

NOTE: .env file used to load environment variables in config.py

Authors: Thomas Cleary,
"""

import os
import unittest

from flask_migrate import Migrate

from app import create_app, db
from app.models.parking_lot import ParkingLot
from app.models.car_bay import CarBay


# create an application instance with config type defined in env variable
# (or default type - development)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# add migration engine to app (/migrations created with 'flask db init')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """ Import db models into Flask shell.
    
    This dictionary of models will be imported into the flask shell when
    'flask shell' cli command is used
    """
    return dict(
        db=db,
        ParkingLot=ParkingLot, CarBay=CarBay
    )


@app.cli.command()
def test():
    """ Create 'flask test' command
    
    Defines a flask command 'flask test' to run unit tests from cmd line 
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
