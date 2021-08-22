from app import db, create_app
from app.models.user import User, Role
from app.models.parking_lot import ParkingLot
from app.models.car_bay import CarBay
import csv


def add_admin_and_roles():

    app = create_app('heroku')

    with app.app_context():
        Role.insert_roles()

        admin = User(
            email="test@uwa.edu.au",
            password = "admin",
            first_name = "Uni",
            last_name = "Park",
            role_id = Role.query.filter_by(name="admin").first().id
        )

        db.session.add(admin) 
        db.session.commit()


def add_parking_lots_bays():
    """ add relevant UWA parking lots to db """

    parking_lot_filename = "./parking-lots.csv"

    # get parking lot numbers from  csv file
    with open(parking_lot_filename, "r") as lotnums_csv:
        lotnums_csvreader = csv.reader(lotnums_csv, delimiter=",")

        # skip column names
        next(lotnums_csvreader)

        # add parking lot to db
        app = create_app('heroku')
        with app.app_context():

            for row in lotnums_csvreader:
                lot_num, num_bays = tuple(row)

                try:
                    lot_num  = int(lot_num)
                    num_bays = int(num_bays)

                except ValueError as error:
                    pass

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


def  main():
    add_admin_and_roles()
    add_parking_lots_bays()


if __name__ == "__main__":
    main()