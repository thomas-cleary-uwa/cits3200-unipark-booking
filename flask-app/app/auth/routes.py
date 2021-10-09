""" Routes used by auth blueprint

Authors: Thomas Cleary,
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from ..models.user import User
from . import auth
from .forms import LoginForm
from .helpers import attempt_log_in



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ route to enable user to login to the application

    This is the first route the user will view when accessing the application.
    """
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return attempt_log_in(login_form)

    return render_template('auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    """ Logs an authenticated user out of the application """
    logout_user()
    return redirect(url_for('auth.login'))
