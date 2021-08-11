""" Initialises an Application instance

    Authors: Thomas Cleary,
"""

from flask import Flask

from config import configs

# initialise flask extensions here
# eg db = SQLAlchemy()


def create_app(config_name):
    """ create and return an instance of the flask application """
    # initialise the flask app
    app = Flask(__name__)

    # configure the app
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    # initalise flask extensions
    # eg db.init(app)

    # import blueprints here to avoid circular imports
    from .main import main as main_bp

    # register blueprints
    app.register_blueprint(main_bp)

    return app