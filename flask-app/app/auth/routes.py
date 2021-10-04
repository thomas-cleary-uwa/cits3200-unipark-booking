""" Routes used by auth blueprint

Authors: Thomas Cleary,
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from ..models.user import User
from . import auth
from .forms import LoginForm
from .helpers import (attempt_log_in,
    get_account, get_change_password_form,
    get_edit_profile_form,edit_profile,edit_password
)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ route to enable user to login to the application

    This is the first route the user will view when accessing the application.
    """
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return attempt_log_in(login_form)

    return render_template('auth/login.html', login_form=login_form)


@auth.route("/account/<int:user_id>", methods=['GET', 'POST'])
@login_required
def account(user_id):
    """ route to enable user to change their password or profile """

    """ provide a form to edit account with id = id """
    edit_account_form = get_edit_profile_form()

    is_redirect, editing_account = get_account(user_id)

    if is_redirect: 
        return editing_account

    if edit_account_form.validate_on_submit():
        return edit_profile(edit_account_form, editing_account)

    # set form defaults
    edit_account_form.email.default      = editing_account.email
    edit_account_form.first_name.default = editing_account.first_name
    edit_account_form.last_name.default  = editing_account.last_name
    edit_account_form.role.default       = editing_account.role.name

    if editing_account.department is not None:
        edit_account_form.department.default = editing_account.department.name

    edit_account_form.process()
    return render_template("auth/account.html",editing_account=editing_account,edit_account_form=edit_account_form)


@auth.route("/change_password/<int:user_id>", methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """ route to enable user to change their password or profile """

    """ provide a form to edit account with id = id """
    change_password_form = get_change_password_form()

    is_redirect, editing_account = get_account(user_id)

    if is_redirect: 
        return editing_account

    if change_password_form.validate_on_submit():
        edit_password(change_password_form, editing_account)
        return redirect(url_for('auth.login'))


    change_password_form.process()

    return render_template("auth/change_password.html",editing_account=editing_account,change_password_form=change_password_form)


@auth.route('/logout')
@login_required
def logout():
    """ Logs an authenticated user out of the application """
    logout_user()
    return redirect(url_for('auth.login'))
