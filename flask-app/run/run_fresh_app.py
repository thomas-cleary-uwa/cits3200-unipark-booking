""" Script to run a fresh version of the application

NOTE: Run this when you are in /flask-app, NOT /run
(path variables are set for this)

Authors: Thomas Cleary,
"""

import os
import csv
import sys
import subprocess

# add flask-app to sys path to allow for app package import
sys.path.append("../flask-app")

# ignore pylint errors, above line adds the package to the system path at runtime
from app import db, create_app
from app.models.bays import ParkingLot, CarBay


def make_fresh_db():
    """ create a fresh instance of the database """
    commands = [
        'rm db-dev.sqlite',
        'flask db migrate',
        'flask db upgrade',
    ]

    if not os.path.exists('db-dev.sqlite'):
        commands = commands[1:]

    for cmd in commands:
        # try and run the command
        try:
            print("\n- ", cmd, sep="")
            exit_value = subprocess.run(cmd.split(), check=True)
            print("Exit Value: {}".format(exit_value))

        # print an error message if the return code is not 0
        except subprocess.CalledProcessError as error:
            print("Error: {}".format(error))

    print() # final newline


def add_parking_lots_bays():
    """ add relevant UWA parking lots to db """

    parking_lot_filename = "run/parking-lots.csv"

    # get parking lot numbers from  csv file
    with open(parking_lot_filename, "r") as lotnums_csv:
        lotnums_csvreader = csv.reader(lotnums_csv, delimiter=",")

        # skip column names
        next(lotnums_csvreader)
        
        # add parking lot to db
        app = create_app('development')
        with app.app_context():

            for row in lotnums_csvreader:
                lot_num, num_bays = tuple(row)

                try:
                    lot_num  = int(lot_num)
                    num_bays = int(num_bays)

                except ValueError as error:
                    print(error)

                new_lot = ParkingLot(lot_number = lot_num)
                db.session.add(new_lot)
                db.session.commit()

                for bay_num in range(1, num_bays+1):
                    new_bay = CarBay(
                        bay_number = bay_num,
                        parking_lot_id = new_lot.id
                    )
                    db.session.add(new_bay)
                db.session.commit()
                
            print("- Parking Lots added to db.\n")
            print("- Car Bays added to db.\n")


def main():
    """ Runs a fresh version of the app.

    - delete db-dev.sqlite
    - create new db.dev.sqlite

    - add Parking Lots to db

    - run the flask app
    """

    make_fresh_db()
    add_parking_lots_bays()

    subprocess.run('flask run'.split(), check=False)


if __name__ == "__main__":
    main()
