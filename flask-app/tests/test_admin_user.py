""" Tests associated with the admin user of the application

Authors: Thomas Cleary,
"""

import unittest

from flask_login import current_user

from app import create_app, db
from app.models.user import User, Role


class AdminTestCases(unittest.TestCase):
    """ tests to run to ensure the admin account is functional """

    def setUp(self):
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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_admin_exists(self):
        """ test the admin user exists in the db

        Test that there is at least one user who is an admin in the database.
        Test that this admin user has: 
            - first_name "Test", last_name="Admin", role_id=<role id of admin user>
        """

        admin_role = Role.query.filter_by(name='admin').first()

        # Test that the admin exists
        self.assertTrue(admin_role is not None)

        # Test that there name is correct
        self.assertTrue(User.query.filter_by(
            email=self.app.config["ADMIN_EMAIL"],
            first_name='Test', last_name='Admin',
            role_id=admin_role.id) is not None)


    def test_admin_can_login_out(self):
        """ test that the admin can log in and out """
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
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_administrator())
            self.assertTrue(current_user.id == admin_user.id)

            # logout
            test_client.get('auth/logout', follow_redirects=True)
            self.assertTrue(current_user.is_anonymous)


    def test_regular_user_not_admin(self):
        """ test that a regular user is not given admin permission when logged in """
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
            self.assertTrue(current_user.is_authenticated)
            self.assertFalse(current_user.is_administrator())
            self.assertTrue(current_user.id == regular_user.id)

            # logout
            test_client.get('auth/logout', follow_redirects=True)
            self.assertTrue(current_user.is_anonymous)

