""" Defines Flask App Instance.

Defines the Flask application instance and some tasks to help manage it.
This file will be executed when the 'flask run' command is used.

NOTE: .env file used to load environment variables in config.py

Authors: Thomas Cleary,
"""

import os
import unittest

from flask_migrate import Migrate, upgrade, migrate

from app import create_app, db

# import models
from app.models.parking_lot import ParkingLot
from app.models.car_bay import CarBay
from app.models.user import Role, User



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
        ParkingLot=ParkingLot, CarBay=CarBay,
        Role=Role, User=User
    )


@app.cli.command()
def test():
    """ Create 'flask test' command
    
    Defines a flask command 'flask test' to run unit tests from cmd line 
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command("add-roles")
def add_roles():
    """ add user roles to the application db """
    Role.insert_roles()


@app.cli.command("add-bays")
def add_bays():
    bays = {
        9 : 12,
        12 : 6,
        19 : 3,
        22 : 11
    }

    for lot_num in bays:
        new_lot = ParkingLot(lot_number=lot_num)
        db.session.add(new_lot)
        db.session.commit()

        for bay_num in range(1, bays[lot_num]+1):
            new_bay = CarBay(
                bay_number = bay_num,
                parking_lot_id = new_lot.id
            )
            db.session.add(new_bay)
        db.session.commit()



@app.cli.command("upgrade-db")
def upgrade_db():
    upgrade()


@app.cli.command("add-admin")
def add_admin():
    admin_user = User(
        email = app.config['ADMIN_EMAIL'],
        password = app.config['ADMIN_PASSWORD'],
        first_name = 'Uni',
        last_name = 'Park',
        role_id = Role.query.filter_by(name='admin').first().id
    )

    db.session.add(admin_user)
    db.session.commit()


@app.cli.command("deploy-app")
def deploy():
    upgrade_db()
    add_roles()
    add_admin()
    add_bays()