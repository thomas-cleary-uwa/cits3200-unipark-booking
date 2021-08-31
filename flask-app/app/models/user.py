""" Models that relate to the users of the application

Authors: Thomas Cleary,
"""

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db, login_manager


class Permission:
    """ Access permission levels as powers of 2 for Role model """
    MAKE_BOOKING = 1
    ADMIN        = 2

    # using this class so in future can expand permissions of different users
    # if necessary



class Role(db.Model):
    """ Represents a role a user of the application can have """
    __tablename__ = 'Role'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)


    # Attributes
    name    = db.Column(db.String(64), unique=True)
    # default is true for only one role
    default = db.Column(db.Boolean, default=False, index=True)
    # use powers of 3 to allow for combinations of permissions
    permissions = db.Column(db.Integer)


    # Relationships
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __repr__(self):
        return "<Role - {}>".format(self.name)


    @staticmethod
    def get_role_names():
        """ return a list of role names """
        return [role.name for role in Role.query.all()]


    @staticmethod
    def insert_roles():
        """ method to insert roles into the db when setting the up the application """
        # use dictionary to store list of permissions
        # permission class to be added later
        roles = {
            'disabled' : [],
            'user'     : [Permission.MAKE_BOOKING],
            'admin'    : [Permission.ADMIN]
        }

        default_role = 'User'

        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)

            role.reset_permissions()
            for permission in roles[role_name]:
                role.add_permission(permission)

            role.default = (role.name == default_role)

            db.session.add(role)
        db.session.commit()


        # permission methods
    def add_permission(self, perm):
        """ add a permission to a role """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """ remove a permission from a role """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """ remove all permissions from the role """
        self.permissions = 0

    def has_permission(self, perm):
        """ return true if role has the permission 'perm' """
        return self.permissions & perm == perm



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
    password_hash = db.Column(db.String(64), unique=True, index=True)


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


    # permission checking methods
    def can(self, permission):
        """ return true if user has permission 'perm' else false """
        return self.role is not None and self.role.has_permission(permission)

    def is_administrator(self):
        """ return true if user is an admin else false """
        return self.can(Permission.ADMIN)



class AnonymousUser(AnonymousUserMixin):
    """ Enable the use of can() and is_administrator() with flask-login's current_user """
    
    def can(self, permission):
        """ return true if anonymous user has permission 'permission'
            else false
        """
        return False

    def is_administrator(self):
        """ return false as anonymous user cannot be an admin """
        return False



@login_manager.user_loader
def load_user(user_id):
    """ flask-login calls this when retrieving info about the user.

    Decorator registers this function with flask-login.
    Returns the user object of user_id is a valid identifier,
    else returns None.
    """
    return User.query.get(int(user_id))
