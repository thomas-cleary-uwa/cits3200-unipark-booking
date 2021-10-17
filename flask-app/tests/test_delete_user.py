""" Tests associated with the admin's 'delete user' functionality.

Authors: Elon Li,
"""
import unittest

from app import create_app, db
from app.models.user import User, Role
from flask_login import current_user

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

        admin_user2 = User(
            email      = self.app.config["ADMIN2_EMAIL"],
            password   = self.app.config["ADMIN2_PASSWORD"],
            first_name = "Test2",
            last_name  = "Admin2",
            role_id    = Role.query.filter_by(name='admin').first().id
        )
        db.session.add(admin_user2)
        
        regular_user = User(
            email      = "test.user@uwa.edu.au",
            password   = "user1234",
            first_name = "Test",
            last_name  = "User",
            role_id    = Role.query.filter_by(name="user").first().id
        )
        db.session.add(regular_user)

        regular_user2 = User(
            email      = "test.user2@uwa.edu.au",
            password   = "user1234",
            first_name = "Test2",
            last_name  = "User2",
            role_id    = Role.query.filter_by(name="user").first().id
        )
        db.session.add(regular_user2)

        disabled_user = User(
            email      = "test.disableduser@uwa.edu.au",
            password   = "user1234",
            first_name = "Testd",
            last_name  = "Userd",
            role_id    = Role.query.filter_by(name="disabled").first().id
        )
        db.session.add(disabled_user)

        disabled_user2 = User(
            email      = "test.disableduser2@uwa.edu.au",
            password   = "user1234",
            first_name = "Testd",
            last_name  = "Userd",
            role_id    = Role.query.filter_by(name="disabled").first().id
        )
        db.session.add(disabled_user2)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_can_delete(self):
        """admin users can delete all types of users execpt themselves if 
        they are the last admin user in the database"""
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
        
            # attempt to delete a regular User
            # get the regular user 
            # from setup() 
            regular_user_email = "test.user@uwa.edu.au"
            user_id = User.query.filter_by(email=regular_user_email).first().id

            test_client.post(
                'admin/delete-user/{}'.format(user_id),
                follow_redirects=True
            )

            the_user_gets_deleted = User.query.filter_by(email=regular_user_email).first()
            self.assertTrue(the_user_gets_deleted is None) # Check the query returned None
            
            # attempt to delete a disabled user
            # get the disabled user 
            # from setup()
            disabled_user_email = "test.disableduser@uwa.edu.au"
            disabled_user_id = User.query.filter_by(email=disabled_user_email).first().id

            test_client.post(
                'admin/delete-user/{}'.format(disabled_user_id),
                follow_redirects=True
            )

            the_disabled_user_deleted = User.query.filter_by(email=disabled_user_email).first()
            self.assertTrue(the_disabled_user_deleted is None) # Check the query returned None


            # attempt to delete another admin user 
            # while there are more than one admin in the database
            admin2_email = self.app.config["ADMIN2_EMAIL"]
            admin2_id = User.query.filter_by(email=admin2_email).first().id
            
            test_client.post(
                "admin/delete-user/{}".format(admin2_id),
                follow_redirects=True
            )

            admin2_deleted = User.query.filter_by(email=admin2_email).first()
            self.assertTrue(admin2_deleted is None) # Check the query returned None

            # attempt to delete themselves when
            # they are the last admin
            admin_user_email = self.app.config["ADMIN_EMAIL"]
            admin_id = User.query.filter_by(email=admin_user_email).first().id

            test_client.post(
                'admin/delete-user/{}'.format(admin_id),
                follow_redirects=True
            )

            admin_deleted = User.query.filter_by(email=admin_user_email).first()
            self.assertFalse(admin_deleted is None) # Check the query returned admin obj
            self.assertTrue(admin_deleted.is_administrator()) # Check the admin is still admin
            self.assertTrue(current_user.is_anonymous) # Check no one is logged in
        #logout
            test_client.get('auth/logout', follow_redirects=True)
    
    def regular_user_cannot_delete(self):
        # get all types of users from SetUp() 
        email      = "test.user@uwa.edu.au"
        password   = "user1234"

        admin_email = self.app.config["ADMIN_EMAIL"]

        email_reg2 = "test.user2@uwa.edu.au"
        
        email_disabled = "test.disableduser@uwa.edu.au"

        regular_user = User.query.filter_by(email=email).first()
        self.assertTrue(regular_user is not None)

        # get the user id for each of them
        admin_id         = User.query.filter_by(email=admin_email).first().id
        regular_user2_id = User.query.filter_by(email=email_reg2).first().id
        diabled_user_id = User.query.filter_by(email=email_disabled).first().id
        
        with self.app.test_client() as test_client:
            # log the regular user in
            test_client.post(
                'auth/login',
                data=dict(email=email, password=password), follow_redirects=True
            )
            
            # attempt to delete the regular user2, 
            # the disabled user and an admin user. 
            test_client.post(
                'admin/delete-user/{}'.format(regular_user2_id),
                follow_redirects=True
            )
            test_client.post(
                'admin/delete-user/{}'.format(diabled_user_id),
                follow_redirects=True
            )
            test_client.post(
                'admin/delete-user/{}'.format(admin_id),
                follow_redirects=True
            )
            
            admin = User.query.filter_by(email=admin_email).first()
            reg_user_2 = User.query.filter_by(email=email_reg2).first()
            dis_user   = User.query.filter_by(email=email_disabled).first()
            
            # Check these users are not deleted by a regular user
            self.assertFalse(reg_user_2 is None) 
            self.assertFalse(dis_user is None)
            self.assertFalse(admin is None)

            #logout
            test_client.get('auth/logout', follow_redirects=True)
    
    def test_delete_bookings_associated_with_users():
        pass