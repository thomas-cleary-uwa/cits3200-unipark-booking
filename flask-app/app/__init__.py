""" Initialises an Application instance

Authors: Thomas Cleary,
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configs

# initialise flask extensions here
db = SQLAlchemy()


def create_app(config_name):
    """ Create and return an instance of the Flask application. """
    # initialise the flask app
    app = Flask(__name__)

    # configure the app
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    # initalise flask extensions
    db.init_app(app)

    # import blueprints here to avoid circular imports
    from .main import main as main_bp

    # register blueprints
    app.register_blueprint(main_bp)

    return app