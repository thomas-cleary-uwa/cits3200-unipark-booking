from app import db
from app.models.user import User, Role


def add_admin_and_roles():
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


def  main():
    add_admin_and_roles()


if __name__ == "__main__":
    main()