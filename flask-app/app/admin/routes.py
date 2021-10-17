""" Admin only accessible routes

Authors: Thomas Cleary,
"""

from datetime import date

from flask import redirect, render_template, url_for, flash
from flask_login import current_user, login_required
from wtforms import SelectField

from app import db

from ..helpers.decorators import admin_required
from ..models.user import User, Role, Department
from . import admin
from .forms import AddUserForm, EditUserForm, AddDepartmentForm, EditDepartmentForm
from .helpers import (
    get_all_users, get_add_user_form, add_new_user,
    get_edit_user_form, get_user, edit_user_info,
    del_user, add_new_department, edit_dep, 
    get_dep, del_dep
)


@admin.route("/index")
@admin.route("/")
@login_required
@admin_required
def index():
    """ home route for admin users """
    return redirect(
        url_for(
            "bookings.parking_lots"
        ))


##############################################################################
# User Routes ################################################################
##############################################################################
@admin.route("/users")
@login_required
@admin_required
def users():
    """ route for admin to see list of all users """
    admin_users, normal_users, disabled_users = get_all_users()

    return render_template("admin/users.html", 
        admin_users=admin_users, 
        normal_users=normal_users,
        disabled_users=disabled_users
    )


@admin.route("/add-user", methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """ route for admin user to create new account """

    add_user_form = get_add_user_form()

    if add_user_form.validate_on_submit():
        redirect_obj = add_new_user(add_user_form)
        return redirect_obj

    # Set form defaults
    add_user_form.role.default = "user"
    add_user_form.department.default = "UniPark"
    add_user_form.process()
    
    return render_template('admin/add_user.html', add_user_form=add_user_form)


@admin.route("/edit-user/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """ provide a form to edit / delete the user with id = id """
    edit_user_form = get_edit_user_form()

    is_redirect, editing_user = get_user(user_id)
    if is_redirect: 
        return editing_user

    if edit_user_form.validate_on_submit():
        return edit_user_info(edit_user_form, editing_user)

    # set form defaults
    edit_user_form.email.default      = editing_user.email
    edit_user_form.first_name.default = editing_user.first_name
    edit_user_form.last_name.default  = editing_user.last_name
    edit_user_form.contact.default    = editing_user.contact_number
    edit_user_form.role.default       = editing_user.role.name

    if editing_user.department is not None:
        edit_user_form.department.default = editing_user.department.name

    edit_user_form.process()
    
    return render_template("admin/edit_user.html", 
        edit_user_form=edit_user_form,
        editing_user=editing_user)


@admin.route("/delete-user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    """ route to perform deletion of user from db """
    return del_user(user_id)


###############################################################################
# Department Routes ###########################################################
###############################################################################
@admin.route("/departments")
@login_required
@admin_required
def departments():
    """ route to display all departments """
    # get list of departments sorted alphabetically
    all_deps = sorted(Department.query.all(), key=lambda x: x.name.lower())
    return render_template("admin/departments.html", departments=all_deps)


@admin.route("/add-department", methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = AddDepartmentForm()

    if form.validate_on_submit():
        return add_new_department(form)

    return render_template("admin/add_department.html", form=form)


@admin.route("/edit-department/<int:department_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(department_id):
    form = EditDepartmentForm()

    is_redirect, editing_dep = get_dep(department_id)
    if is_redirect:
        return edit_department

    if form.validate_on_submit():
        return edit_dep(editing_dep, form)

    # set form defaults
    form.name.default = editing_dep.name
    form.process()

    return render_template("admin/edit_department.html", form=form, editing_dep=editing_dep)


@admin.route("/delete-department/<int:department_id>")
@login_required
@admin_required
def delete_department(department_id):
    return del_dep(department_id)
