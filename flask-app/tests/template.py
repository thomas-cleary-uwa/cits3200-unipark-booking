""" Template for a unittest TestCase

Authors: Thomas Cleary,
"""

import unittest

from app import create_app, db
from app.models.user import User, Role


class AdminTestCases(unittest.TestCase):
    """ tests to run to ensure the admin account is functional
    
    This sets up the testing environment
    """

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

        # Add more things to db here

        db.session.commit()

        
    def tearDown(self):
        # get rid of the testing environment
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_testname(self):
        """ this is a test that this file will run
        
        function name important "def test_<test name>(self)"
        """
        pass
        # eg self.assertTrue(boolean expression expected to be true)



