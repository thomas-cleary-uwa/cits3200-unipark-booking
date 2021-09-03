""" Routes used by auth blueprint

Authors: Thomas Cleary,
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth
from .forms import LoginForm
from ..models.user import User



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ route to enable user to login to the application

    This is the first route the user will view when accessing the application.
    """
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data.strip()).first()

        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            next_route = request.args.get('next')

            if next_route is None or not next_route.startswith('/'):
                next_route = url_for('main.index')

            # Post/Redirect/Get pattern
            return redirect(next_route)

        flash('Invalid username or password.')

    return render_template('auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    """ Logs an authenticated user out of the application """
    logout_user()
    return redirect(url_for('auth.login'))
