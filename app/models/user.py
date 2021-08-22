""" Models that relate to the users of the application

Authors: Thomas Cleary,
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db, login_manager



class Role(db.Model):
    """ Represents a role a user of the application can have """
    __tablename__ = 'Role'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Attributes
    name    = db.Column(db.String(64), unique=True)
    #
    # default is true for only one role
    default = db.Column(db.Boolean, default=False, index=True)

    # Relationships
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __repr__(self):
        return "<Role - {}>".format(self.name)


    @staticmethod
    def insert_roles():
        """ method to insert roles into the db when setting the up the application """
        # use dictionary to store list of permissions
        # permission class to be added later
        roles = {
            'disabled' : [],
            'user'     : [],
            'admin'    : []
        }

        default_role = 'User'

        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)

            role.default = (role.name ==default_role)

            db.session.add(role)
        db.session.commit()



class User(UserMixin, db.Model):
    """ Represents a user of the application

    Subclasses:
        - UserMixin: for is_authenticated(), is_active(), is_anonymous()...
        - db.Model:  to define a table for the database
    """
    __tablename__ = 'User'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication Attributes
    email         = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(256), unique=True, index=True)


    # Profile Attributes
    first_name = db.Column(db.String(64), index=True)
    last_name  = db.Column(db.String(64), index=True)

    # Foreign Keys
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))


    # Relationships
    # (bookings)

    @property
    def password(self):
        """ 'password' getter method
        Throw an error as we should not be able to access a plaintext password
        """
        raise AttributeError("'password' is not a readable attribute.")

    @password.setter
    def password(self, password):
        """ 'password' setter method """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ return true if hash(password) equals this user's password_hash, else false. """
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return "<User {} - {} {} ({})>".format(
            self.id,
            self.first_name, self.last_name,
            self.role.name
        )



@login_manager.user_loader
def load_user(user_id):
    """ flask-login calls this when retrieving info about the user.

    Decorator registers this function with flask-login.
    Returns the user object of user_id is a valid identifier,
    else returns None.
    """
    return User.query.get(int(user_id))
