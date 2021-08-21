""" Configuration classes for an application instance

Authors: Thomas Cleary,
"""

import os
from dotenv import load_dotenv

# path to /flask-app
basedir = os.path.abspath(os.path.dirname(__file__))

# load environement variables from .env for creating fresh instances of the app
load_dotenv()


class Config:
    """ Base class for Flask app configuration """

    # Flask uses this to protect the user session against tampering
    # (CSRF attacks)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    # The Flask-SQLAlchemy documentation suggests setting key
    # SQLALCHEMY_TRACK_MODIFICATIONS to False to use less memory
    # unless signals for object changes are needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """ Can be used as an additional way to customise the application's
            configuration
        """
        return



class DevelopmentConfig(Config):
    """ Configuration to be used during development of the application """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
                              or \
                              'sqlite:///' + os.path.join(basedir, 'db-dev.sqlite')



class TestingConfig(Config):
    """ Configuration to be used when testing the application """
    # used by test to check if app is in this config
    TESTING = True

    # Cannot test login while enabled
    WTF_CSRF_ENABLED = False

    # Use in memory db instead of file for testing
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
                              or \
                              'sqlite://'



class ProductionConfig(Config):
    """ Configuration to be used by the production version of the application """
    # will most certainly change from .sqlite to something else in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                              or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')



configs = {
    'development': DevelopmentConfig,
    'testing'    : TestingConfig,
    'production' : ProductionConfig,

    'default'    : DevelopmentConfig
}
