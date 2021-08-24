""" Admin only accessible routes

Authors: Thomas Cleary,
"""

from flask import redirect, render_template, url_for, flash
from flask_login import current_user, login_required
from wtforms import SelectField

from app import db

from ..helpers.decorators import admin_required
from ..models.user import User, Role
from . import admin
from .forms import AddUserForm



@admin.route("/admin")
@login_required
@admin_required
def index():
    """ home route for admin users """
    return render_template("admin/index.html")


@admin.route("/users")
@login_required
@admin_required
def users():
    """ route for admin to see list of all users """
    all_users = User.query.all()
    return render_template("admin/users.html", users=all_users)


@admin.route("/add-user", methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """ route for admin user to create new account """

    role = SelectField("Role: ", choices=Role.get_role_names())
    setattr(AddUserForm, 'role', role)
    add_user_form = AddUserForm()

    if add_user_form.validate_on_submit():
        email = add_user_form.email.data.lower()
        password = add_user_form.password.data

        names = email.split("@")[0].split(".")
        first_name = names[0].capitalize()
        last_name = names[1].capitalize()

        role_name = add_user_form.role.data

        # NOTE currently form not dynamically getting list of roles so is hard coded as
        # user = 1, admin = 2
        # please fix this

        new_user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role_id = Role.query.filter_by(name=role_name).first().id
        )
        db.session.add(new_user)
        db.session.commit()

        flash("User Creation Successful.")
        return redirect(url_for('admin.users'))
    
    return render_template('admin/add_user.html', add_user_form=add_user_form)