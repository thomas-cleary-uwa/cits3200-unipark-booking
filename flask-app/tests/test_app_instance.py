"""
Basic test cases for the Flask app

Authors: Thomas Cleary,
"""

import unittest

from flask import current_app
from app import create_app, db



class FlaskAppInstanceTestCase(unittest.TestCase):
    """ basic test cases for Flask application instance """

    def setUp(self):
        self.app = create_app('testing') # use db in memory

        # ensures tests have access to current_app variable
        # (like regular requests do)
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create new db
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_app_exists(self):
        """ test the application instance exists """
        self.assertFalse(current_app is None)


    def test_app_is_testing(self):
        """ test that the app instance is in the 'TESTING' config state """
        self.assertTrue(current_app.config['TESTING'])
