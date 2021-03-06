""" Initialises an Application instance

Authors: Thomas Cleary,
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import configs

# initialise flask extensions here
db = SQLAlchemy()

login_manager = LoginManager()
# tell flask-login what login route is
# will redirect an anonymous user here if they attempt to access a protected
# page.
login_manager.login_view = 'auth.login'

mail = Mail()


def create_app(config_name):
    """ Create and return an instance of the Flask application. """
    # initialise the flask app
    app = Flask(__name__)

    # configure the app
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    # initalise flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import blueprints here to avoid circular imports
    from .main import main as main_bp
    from .auth import auth as auth_bp
    from .admin import admin as admin_bp
    from .bookings import bookings as bookings_bp

    # register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")

    return app