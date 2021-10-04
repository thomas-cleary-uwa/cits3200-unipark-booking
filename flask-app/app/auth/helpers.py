""" helper functions for auth routes """

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from wtforms import SelectField
from app import db
from .forms import EditProfileForm,ChangePasswordForm
from ..models.user import User, Role, Department

def attempt_log_in(login_form):
    user = User.query.filter_by(email=login_form.email.data.strip()).first()

    if user is None:
        flash("Invalid username of password.")
        return redirect(url_for("auth.login"))

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


def get_edit_profile_form():
    # Add dynamic fields to the add user form
    role = SelectField("Role: ", choices=Role.get_names(),render_kw={"disabled" : "disabled"},validators=[])
    setattr(EditProfileForm, 'role', role)

    department = SelectField("Department: ", choices=Department.get_names())
    setattr(EditProfileForm, 'department', department) 

    return EditProfileForm()

def get_change_password_form():
    return ChangePasswordForm()

def get_account(user_id):
    editing_account = User.query.get(user_id)
    return (False, editing_account)

def edit_password(change_password_form,edit_account):
    email_check_user = User.query.filter_by(email=edit_account.email).first()
    email_check_user.password=change_password_form.password.data.strip()
    db.session.commit()

def edit_profile(edit_account_form,edit_account):
    # check if email exists in database and is not the same as editing user
    email_check_user = User.query.filter_by(email=edit_account.email).first()
    if email_check_user is not None and email_check_user.id != edit_account.id:
        flash("The entered email address is already in use.")
        return redirect(url_for("auth.account", user_id=edit_account.id))

    edit_account.department_id = Department.query.filter_by(name=edit_account_form.department.data).first().id

    db.session.commit()

    flash("Account Details Successfully Updated.")
    return redirect(url_for('auth.account', user_id=edit_account.id))