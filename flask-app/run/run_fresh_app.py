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
import random
import re

from hashlib import md5
from datetime import datetime, date, timedelta

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

    pdf_path = "./app/static/reservation_signs/"
    if os.path.exists(pdf_path):
        for f in os.listdir(pdf_path):
            if re.search(r'^.*\.pdf$', f):
                os.remove(os.path.join(pdf_path, f))

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
    app = create_app('setup')

    with app.app_context():
        new_user = User(
            email = app.config["TEST_USER_EMAIL"],
            password = app.config["TEST_USER_PASSWORD"],
            first_name = 'Test',
            last_name = 'User',
            role_id = Role.query.filter_by(name='user').first().id,
            department_id = Department.query.all()[0].id
        )

        db.session.add(new_user)
        db.session.commit()
        print("{}- Regular user added.{}\n".format(
            bColours.OKGREEN, bColours.ENDC
        ))


def add_user_bookings(num_bookings):
    """ add a booking for the test user """

    app = create_app("setup")
    with app.app_context():

        user_email = app.config["TEST_USER_EMAIL"]
        user_password = app.config["TEST_USER_PASSWORD"]

        with app.test_client() as test_client:
            # log the admin user in
            test_client.post(
                'auth/login',
                data=dict(email=user_email, password=user_password), 
                follow_redirects=True
            )

            for _ in range(num_bookings):
                datetime_placed = datetime.now()

                all_bays = CarBay.query.all()
                choice = random.randint(0, len(all_bays)-1)
                
                # get bay id
                bay = all_bays[choice]
                bay_num = bay.bay_number
                lot_num = bay.lot.lot_number

                # get timeslots
                start = random.randint(1, 32)
                end   = random.randint(start, 32)

                # get date booked
                date_booked = date.today() + timedelta(days=random.randint(0, 6))

                test_client.post(
                    "bookings/confirm/{}/{}/{}/{}/{}/{}/{}".format(
                        lot_num, bay_num, 
                        date_booked.day, date_booked.month, date_booked.year,
                        start, end
                    ),
                    data=dict(
                        title="Mr.",
                        guest_first_name="Test",
                        guest_last_name="User",
                        vehicle_rego="T3STU53R",
                        ts_and_cs=True
                    )
                )

    
        print("{}- Test user bookings added ({} attempted)\n{}\n".format(
            bColours.OKGREEN, num_bookings, bColours.ENDC
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
    parser.add_argument("-b", "--booking", type=int, help="generate a booking for the test user")
    parser.parse_args()

    args = parser.parse_args()
    if args.booking and not args.add_user:
        parser.error("--booking can only be used with --add-user")

    make_fresh_db()
    add_departments()
    add_admin()
    add_parking_lots_bays()

    if args.add_user:
        add_user()
        if args.booking:
            add_user_bookings(args.booking)

    subprocess.run('flask run --host 0.0.0.0'.split(), check=False)


if __name__ == "__main__":
    main()
