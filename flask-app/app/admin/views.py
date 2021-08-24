""" Admin only accessible routes

Authors: Thomas Cleary,
"""

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db

from ..helpers.decorators import admin_required
from ..models.user import User
from . import admin
from .forms import AddUserForm



@admin.route("/users")
@login_required
@admin_required
def users():
    """ route for admin to see list of all users """
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin.route("/add-user")
@login_required
@admin_required
def add_user():
    """ route for admin user to create new account """
    add_user_form = AddUserForm()

    if add_user_form.validate_on_submit():
        # add user to db
        # flask confirmation
        # redirect back to user list
        return redirect(url_for('admin.users'))
    
    return render_template('admin/add_user.html', add_user_form=add_user_form)