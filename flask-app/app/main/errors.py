""" Error handling for main blueprint """

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(error):
    """ renders template for 404 page not found error
        (1 positional argument required by decorator,
            error = werkzeug exception object)
    """
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(error):
    """ renders template for 500 internal server error
        (1 positional argument required by decorator,
            error = werkzeug exception object)
    """
    return render_template('errors/500.html'), 500