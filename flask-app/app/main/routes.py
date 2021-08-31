""" Routes used by main blueprint

Authors: Thomas Cleary,
"""

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main


@main.route('/')
@main.route('/index')
@login_required
def index():
    """ Initial route for the application. """
    if current_user.is_administrator():
        return redirect(url_for("admin.index"))
    return render_template('main/index.html')
