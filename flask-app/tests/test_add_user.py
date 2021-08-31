""" Tests associated with the admin's 'add user' functionality.

Authors: Thomas Cleary,
"""

import unittest

from app import create_app, db
from app.models.user import User, Role


class AddUserTestCases(unittest.TestCase):
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


    def test_admin_can_add(self):
        """ test than an admin user can add user accounts
        
        user account types: admin, user, disabled
        """
        # get the admin user
        # from SetUp()
        email    = self.app.config["ADMIN_EMAIL"]
        password = self.app.config["ADMIN_PASSWORD"]

        admin_user = User.query.filter_by(email=email).first()
        self.assertTrue(admin_user is not None)

        with self.app.test_client() as test_client:
            # log the admin user in
            test_client.post(
                'auth/login',
                data=dict(email=email, password=password), follow_redirects=True
            )

            # attempt to create a new admin user
            admin_email = "new.admin@uwa.edu.au"
            admin_password = "admin1234" # cannot read password directly from user object

            test_client.post(
                'admin/add-user',
                data=dict(
                    email=admin_email,
                    password=admin_password,
                    password2=admin_password,
                    role="admin")
            )

            inserted_new_admin = User.query.filter_by(
                email=admin_email).first()
            
            self.assertTrue(inserted_new_admin is not None) # Check the query returned a user
            self.assertTrue(inserted_new_admin.is_administrator()) # Check they are admin


            # attempt to create a new  user
            user_email = "new.user@uwa.edu.au"
            user_password = "user1234" # cannot read password directly from user object

            test_client.post(
                'admin/add-user',
                data=dict(
                    email=user_email,
                    password=user_password,
                    password2=user_password,
                    role="user")
            )

            inserted_new_user = User.query.filter_by(
                email=user_email).first()
            
            self.assertTrue(inserted_new_user is not None) # Check the query returned a user
            self.assertFalse(inserted_new_user.is_administrator()) # Check they are not admin
            self.assertTrue(inserted_new_user.role.name == "user") # Check they are a 'user'


            # attempt to create a new  disabled user
            disabled_email = "new.disabled@uwa.edu.au"
            disabled_password = "disabled1234" # cannot read password directly from user object

            test_client.post(
                'admin/add-user',
                data=dict(
                    email=disabled_email,
                    password=disabled_password,
                    password2=disabled_password,
                    role="disabled")
            )

            inserted_new_disabled = User.query.filter_by(
                email=disabled_email).first()
            
            self.assertTrue(inserted_new_disabled is not None) # Check the query returned a user
            self.assertFalse(inserted_new_disabled.is_administrator()) # Check they are not admin
            self.assertTrue(inserted_new_disabled.role.name == "disabled") # Check they are a 'user'

            # logout
            test_client.get('auth/logout', follow_redirects=True)


    def test_user_cannot_add(self):
        """ test that a regular user cannot add user accounts """
        # get the regular user
        # from SetUp()
        email    = "test.user@uwa.edu.au"
        password = "user1234"

        regular_user = User.query.filter_by(email=email).first()
        self.assertTrue(regular_user is not None)

        with self.app.test_client() as test_client:
            # log the regular user in
            test_client.post(
                'auth/login',
                data=dict(email=email, password=password), follow_redirects=True
            )

            # attempt to create a new admin user
            admin_email = "new.admin@uwa.edu.au"
            admin_password = "admin1234" # cannot read password directly from user object

            test_client.post(
                'admin/add-user',
                data=dict(
                    email=admin_email,
                    password=admin_password,
                    password2=admin_password,
                    role="admin")
            )

            inserted_new_admin = User.query.filter_by(
                email=admin_email).first()
            
            self.assertTrue(inserted_new_admin is None) # Check the query returned a user

            # logout
            test_client.get('auth/logout', follow_redirects=True)


