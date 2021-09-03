""" Tests associated with application authentication (login / logout)

Authors: Thomas Cleary,
"""

import unittest

from flask_login import current_user

from app import create_app, db
from app.models.user import User, Role


class AuthenticationTestCases(unittest.TestCase):
    """ a subclass of TestCase for unittest module to run methods (unit tests) """

    def setUp(self):
        # This sets up the testing environment

        # create an application and push its context on the stack
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # setup the database tables (testing db in memory not a file)
        db.create_all()

        Role.insert_roles()

        admin_user = User(
            email      = self.app.config["ADMIN_EMAIL"],
            password   = self.app.config["ADMIN_PASSWORD"],
            first_name = "Test",
            last_name  = "Admin",
            role_id    = Role.query.filter_by(name='admin').first().id
        )
        db.session.add(admin_user)

        regular_user = User(
            email      = "test.user@uwa.edu.au",
            password   = "user1234",
            first_name = "Test",
            last_name  = "User",
            role_id    = Role.query.filter_by(name="user").first().id 
        )
        db.session.add(regular_user)

        db.session.commit()

        
    def tearDown(self):
        # get rid of the testing environment
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_login_logout_admin(self):
        """ test that an admin user can login """
        # from SetUp()
        email    = self.app.config["ADMIN_EMAIL"]
        password = self.app.config["ADMIN_PASSWORD"]

        admin_user = User.query.filter_by(email=email).first()
        self.assertTrue(admin_user is not None)

        with self.app.test_client() as test_client:
            # login
            test_client.post(
                'auth/login',
                data=dict(email=email, password=password), follow_redirects=True
            )
            self.assertTrue(current_user.is_authenticated) # check admin is logged in
            self.assertTrue(current_user.is_administrator()) # check they are admin user
            self.assertTrue(current_user.id == admin_user.id) # check current user id matches admin's

            # logout
            test_client.get('auth/logout', follow_redirects=True)
            self.assertTrue(current_user.is_anonymous) # check no one is logged in

    
    def test_login_logout_user(self):
        """ test that a regular user can login and logout """
        # from SetUp()
        email = "test.user@uwa.edu.au"
        password = "user1234"

        regular_user = User.query.filter_by(email=email).first()
        self.assertTrue(regular_user is not None)

        with self.app.test_client() as test_client:
            # login
            test_client.post(
                'auth/login',
                data=dict(email=email, password=password), follow_redirects=True
            )
            self.assertTrue(current_user.is_authenticated) # check they are logged in
            self.assertTrue(current_user.role.name == "user") # check their role is "user"
            self.assertTrue(current_user.id == regular_user.id) # check that logged in user has corerct id

            # logout
            test_client.get('auth/logout', follow_redirects=True)
            self.assertTrue(current_user.is_anonymous) # check no one is logged in




