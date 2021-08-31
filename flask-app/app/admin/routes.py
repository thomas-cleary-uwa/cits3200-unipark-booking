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
from .forms import AddUserForm, EditUserForm



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

    add_user_form.role.default = "user"
    add_user_form.process() # need to cal this to set new default

    if add_user_form.validate_on_submit():
        email = add_user_form.email.data.lower().strip()
        password = add_user_form.password.data.strip()

        names = email.split("@")[0].split(".")
        first_name = names[0].capitalize().strip()
        last_name = names[1].capitalize().strip()

        role_name = add_user_form.role.data # ignore pylint error, we just added the role member

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


# NOTE: probably change the route <int:id> to be a different slug
# NOTE: Probably want to add reset password functionality at some point
@admin.route("/edit-user/<int:id>")
@login_required
@admin_required
def edit_user(id):
    """ provide a form to edit / delete the user with id = id """
    role = SelectField("Role: ", choices=Role.get_role_names())
    setattr(EditUserForm, 'role', role)

    edit_user_form = EditUserForm()

    editing_user = User.query.get(id)
    if editing_user is None:
        flash("Something went wrong: Could not find this user")
        return redirect(url_for("admin.users"))

    edit_user_form.email.default = editing_user.email
    edit_user_form.role.default = editing_user.role.name
    edit_user_form.process() # need to call this to actually set new default values

    if edit_user_form.validate_on_submit():
        flash("User Details Successfully Updated.")
        return redirect(url_for('admin.users'))
    
    return render_template(
        "admin/edit_user.html", 
        edit_user_form=edit_user_form,
        editing_user=editing_user)


@admin.route("/delete-user/<int:id>")
@login_required
@admin_required
def delete_user(id):
    """ route to perform deletion of user from db """
    delete_user = User.query.get(id)
    if delete_user is None:
        flash("Something went wrong: user could not be found")

    else:
        db.session.delete(delete_user)
        db.session.commit()
        flash("User was successfully deleted.")

    return redirect(url_for("admin.users"))