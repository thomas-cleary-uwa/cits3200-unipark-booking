""" Tests associated with the admin's 'edit user' functionality.

Authors: Elon Li,
"""
import unittest
from ..app import create_app, db
from app.models.user import User, Role, Department
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
        
        regular_user = User(
            email      = "test.user@uwa.edu.au",
            password   = "user1234",
            first_name = "Test",
            last_name  = "User",
            role_id    = Role.query.filter_by(name="user").first().id,
            department_id  = Department.query.filter_by(name='Dental School').first().id
        )
        db.session.add(regular_user)

        disabled_user = User(
            email      = "test.disableduser@uwa.edu.au",
            password   = "user1234",
            first_name = "Testd",
            last_name  = "Userd",
            role_id    = Role.query.filter_by(name="disabled").first().id
        )
        db.session.add(disabled_user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_can_edit(self):
        """admin users can edit all types of users execpt themselves"""
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

            self.assertTrue(current_user.is_authenticated) # Check the user loged in
            self.assertFalse(current_user.is_administrator()) # Check the user is admin
            
            # get a users
            # from setup()
            email      = "test.user@uwa.edu.au"
            new_email  = ""
            first_name  = "Test"
            last_name  = "User"
            user1_id = User.query.filter_by(email=email).first().id
            
            # test that name can be changed' 
            test_client.post(
                "/edit-user/{}".format(user1_id),
                data=dict(first_name='Michael', last_name='Wise'), follow_redirects=True
            )
            user = User.query.get(user1_id)
            self.assertTrue(user.first_name == 'Michael')
            self.assertTrue(user.last_name == 'Wise')

            # test that email can be changed
            test_client.post(
                "/edit-user/{}".format(user1_id),
                data=dict(email=new_email), follow_redirects=True
            )
            self.assertTrue(user.email==new_email)

            # test that role can be changed
            role_id = Role.query.filter_by(name='admin').first().id
            test_client.post(
                "/edit-user/{}".format(user1_id),
                data=dict(role_id=role_id), follow_redirects=True
            )
            self.assertTrue(user.is_administrator()) # check he is admin now

            # test that department can be changed
            dep_id = Department.query.filter_by(name='Business School').first().id
            test_client.post(
                "/edit-user/{}".format(user1_id),
                data=dict(department=dep_id), follow_redirects=True
            )
            self.assertTrue(user.department_id==dep_id)


