""" helper functions for auth routes """

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from ..models.user import User
from . import auth


def attempt_log_in(login_form):
    user = User.query.filter_by(email=login_form.email.data.strip()).first()

    if user.role.name == "disabled":
        flash("Your account is currently disabled")
        return redirect(url_for("auth.login"))

    if user is not None and user.verify_password(login_form.password.data):
        login_user(user)
        next_route = request.args.get('next')

        if next_route is None or not next_route.startswith('/'):
            next_route = url_for('main.index')

        # Post/Redirect/Get pattern
        return redirect(next_route)

    flash('Invalid username or password.')
    return redirect(url_for("auth.login"))