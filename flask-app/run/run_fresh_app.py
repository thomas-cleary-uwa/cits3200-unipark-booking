""" Script to run a fresh version of the application

NOTE: Run this when you are in /flask-app, NOT /run
(path variables are set for this)

Authors: Thomas Cleary,
"""

import os
import csv
import sys
import subprocess
import argparse

from hashlib import md5
from datetime import datetime, date

# add flask-app to sys path to allow for app package import
sys.path.append("../flask-app")

# ignore pylint errors, above line adds the app package to the system path at runtime
from app import db, create_app
from app.models.parking_lot import ParkingLot
from app.models.car_bay import CarBay
from app.models.user import Role, User, Department
from app.models.booking import Booking


class bColours:
    """ codes to make stdout msgs in colour """
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'



def make_fresh_db():
    """ create a fresh instance of the database """
    commands = [
        # create db file from current migrations
        'flask db upgrade',
        # create new migrations from updated models, add message after
        'flask db migrate',
        # update db file with new migrations
        'flask db upgrade',
        # add roles to Role table
        'flask add-roles'
    ]

    db_path = './db-dev.sqlite'
    if os.path.exists(db_path):
        os.remove(db_path)

    for cmd in commands:
        # try and run the command
        try:
            print("\n{}- {}{}".format(
                bColours.HEADER,
                cmd, 
                bColours.ENDC),
                sep=""
            )
            exit_value = subprocess.run(cmd.split(), check=True)
            print("{}Exit Value: {}{}".format(
                bColours.OKBLUE,
                exit_value,
                bColours.ENDC
            ))

        # print an error message if the return code is not 0
        except subprocess.CalledProcessError as error:
            print("{}Error: {}{}".format(
                bColours.WARNING, 
                error,
                bColours.ENDC
            ))

    print("\n{}- Roles added to db.{}\n".format(
        bColours.OKGREEN, bColours.ENDC
    ))



def add_departments():
    """ add departments from departments.txt """
    departments_file = "./run/departments.txt"

    with open(departments_file, "r") as dep_file:
        departments = [line.strip() for line in dep_file]

    with create_app("development").app_context():
        for dep in departments:
            new_dep = Department(
                name = dep
            )
            db.session.add(new_dep)
        
        db.session.commit()

    print("{}- Departments added.{}\n".format(
        bColours.OKGREEN, bColours.ENDC
    ))


def add_admin():
    """ add the admin user to the db """
    app = create_app('development')

    with app.app_context():
        admin_user = User(
            email = app.config['ADMIN_EMAIL'],
            password = app.config['ADMIN_PASSWORD'],
            first_name = 'uni',
            last_name = 'park',
            role_id = Role.query.filter_by(name='admin').first().id,
            department_id = Department.query.filter_by(name="UniPark").first().id
        )

        db.session.add(admin_user)
        db.session.commit()
        print("{}- Admin user added.{}\n".format(
            bColours.OKGREEN, bColours.ENDC
        ))


def add_user():
    """ add a user to the application """
    app = create_app('development')

    with app.app_context():
        new_user = User(
            email = "test.user@uwa.edu.au",
            password = "user1234",
            first_name = 'test',
            last_name = 'user',
            role_id = Role.query.filter_by(name='user').first().id,
            department_id = Department.query.all()[0].id
        )

        db.session.add(new_user)
        db.session.commit()
        print("{}- Regular user added.{}\n".format(
            bColours.OKGREEN, bColours.ENDC
        ))


def add_user_booking():
    """ add a booking for the test user """

    with create_app("development").app_context():

        user_email = "test.user@uwa.edu.au"
        datetime_placed = datetime.now()

        booking_code = md5((str(datetime_placed) + user_email).encode()). \
                       hexdigest()[:10]


        new_booking = Booking(
            booking_code    = booking_code,
            datetime_placed = datetime_placed,
            date_booked     = date.today(),
            timeslot_start  = 1,
            timeslot_end    = 8,
            guest_name      = "Jesus",
            vehicle_rego    = "666-666",
            bay_id          = 1,
            user_id         = User.query.filter_by(first_name="test").first().id
        )

        db.session.add(new_booking)
        db.session.commit()
    
        print("{}- Test user booking added.{}\n".format(
            bColours.OKGREEN, bColours.ENDC
        ))


def add_parking_lots_bays():
    """ add relevant UWA parking lots to db """

    parking_lot_filename = "run/parking-lots.csv"

    # get parking lot numbers from  csv file
    with open(parking_lot_filename, "r") as bay_info_csv:
        bay_info_csvreader = csv.reader(bay_info_csv, delimiter=",")

        # skip column names
        next(bay_info_csvreader)

        # work in an applicatio context
        app = create_app('development')
        with app.app_context():

            added_lot_nums = []

            current_lot_id = None
            num_bays = 1


            for row in bay_info_csvreader:
                lot_num, latitude, longitude = tuple(row)

                try:
                    lot_num   = int(lot_num)
                    latitude  = float(latitude)
                    longitude = float(longitude)

                except ValueError:
                    print("Value in {} could not be converted to int/float".format(
                        parking_lot_filename
                    ))

                if lot_num not in added_lot_nums:
                    # add the parking lot to the db
                    new_lot = ParkingLot(
                        lot_number = lot_num,
                        latitude   = latitude,
                        longitude  = longitude)
                    db.session.add(new_lot)
                    db.session.commit()

                    added_lot_nums.append(lot_num)

                    # change current lot working with
                    current_lot_id = new_lot.id
                    # reset bay count
                    num_bays = 1

                # add the new bay
                new_bay = CarBay(
                    bay_number     = num_bays,
                    latitude       = latitude,
                    longitude      = longitude,
                    parking_lot_id = current_lot_id
                )
                db.session.add(new_bay)
                db.session.commit()

                num_bays += 1

    print("{}- Parking Lots added to db.{}\n".format(
        bColours.OKGREEN, bColours.ENDC
    ))
    print("{}- Car Bays added to db.{}\n".format(
        bColours.OKGREEN, bColours.ENDC
    ))


def main():
    """ Runs a fresh version of the app.

    - delete db-dev.sqlite
    - create new db.dev.sqlite

    - add Roles to db
    - add Departments to db
    - add Admin account to db
    - add Parking Lots and Car Bays to db

    - run the flask app
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--add-user", help="start with a test user", action="store_true")
    parser.add_argument("-b", "--booking", help="generate a booking for the test user", action="store_true")
    parser.parse_args()

    make_fresh_db()
    add_departments()
    add_admin()
    add_parking_lots_bays()

    args = parser.parse_args()

    if args.add_user:
        add_user()
        if args.booking:
            add_user_booking()
    else:
        if args.booking:
            parser.error("--booking can only be used with --add-user")

    subprocess.run('flask run --host 0.0.0.0'.split(), check=False)


if __name__ == "__main__":
    main()
