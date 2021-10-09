""" helper functions for admin route.

Authors: Thomas Cleary,
"""

from flask import flash, redirect, url_for
from flask_login import current_user
from wtforms import SelectField

from app import db

from .forms import AddUserForm, EditUserForm, AddDepartmentForm, EditDepartmentForm
from ..models.user import User, Role, Department


def get_all_users():
    """ return all users by role """
    all_users = User.query.join(Role, User.role_id==Role.id)
    admin_users = all_users.filter(Role.name=="admin")
    normal_users = all_users.filter(Role.name=="user")
    disabled_users = all_users.filter(Role.name=="disabled")

    return (admin_users, normal_users, disabled_users)


def get_add_user_form():
    # Add dynamic fields to the add user form
    role = SelectField("Role: ", choices=Role.get_names())
    setattr(AddUserForm, 'role', role)

    department = SelectField("Department: ", choices=Department.get_names())
    setattr(AddUserForm, 'department', department) 

    return AddUserForm()


def add_new_user(add_user_form):
    """ add the new user to the db """
    email = add_user_form.email.data.lower().strip()
    password = add_user_form.password.data.strip()

    first_name = add_user_form.first_name.data.lower().capitalize()
    last_name = add_user_form.last_name.data.lower().capitalize()

    role_name = add_user_form.role.data # ignore pylint error, we just added the role member
    dep_name = add_user_form.department.data # ignore pylint error, we just added the department member

    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role_id = Role.query.filter_by(name=role_name).first().id,
        department_id = Department.query.filter_by(name=dep_name).first().id
    )
    db.session.add(new_user)
    db.session.commit()

    flash("User Creation Successful.")
    return redirect(url_for('admin.users'))


def get_edit_user_form():
    # Add dynamic fields to the add user form
    role = SelectField("Role: ", choices=Role.get_names())
    setattr(EditUserForm, 'role', role)

    department = SelectField("Department: ", choices=Department.get_names())
    setattr(EditUserForm, 'department', department) 

    return EditUserForm()


def get_user(user_id):
    """ return user, else if not found a redirect to users page """
    editing_user = User.query.get(user_id)
    
    if editing_user is None:
        flash("Something went wrong: Could not find this user")
        return (True, redirect(url_for("admin.users")))
    
    return (False, editing_user)


def edit_user_info(edit_user_form, editing_user):
    # check if email exists in database and is not the same as editing user
    entered_email = edit_user_form.email.data.strip()

    # if the admin user is editing themself
    if current_user == editing_user:
        if edit_user_form.role.data != "admin":
            flash("You cannot change your own role")
            return redirect(url_for("admin.edit_user", user_id=editing_user.id))

    email_check_user = User.query.filter_by(email=entered_email).first()
    if email_check_user is not None and email_check_user.id != editing_user.id:
        flash("The entered email address is already in use.")
        return redirect(url_for('admin.edit_user', user_id=editing_user.id))
    
    editing_user.email = entered_email
    editing_user.first_name = edit_user_form.first_name.data.strip().capitalize()
    editing_user.last_name = edit_user_form.last_name.data.strip().capitalize()
    editing_user.role_id = Role.query.filter_by(name=edit_user_form.role.data).first().id
    editing_user.department_id = Department.query.filter_by(name=edit_user_form.department.data).first().id

    db.session.commit()

    flash("User Details Successfully Updated.")
    return redirect(url_for('admin.users'))


def del_user(user_id):
     # if admin user is trying to delete themself
    if user_id == current_user.id:
        # if they are the last admin, do not let them delete themself
        admin_role_id = Role.query.filter_by(name="admin").first().id
        if User.query.filter_by(role_id=admin_role_id).count() <= 1:
            flash("Deletion of the only admin account not allowed. Make another admin account to delete this one.")
        
        else:
            db.session.delete(current_user)
            db.session.commit()
            return redirect(url_for("auth.logout"))


    else:
        user_to_delete = User.query.get(user_id)
        if user_to_delete is None:
            flash("Something went wrong: user could not be found")

        else:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User <{}> was successfully deleted.".format(user_to_delete.email))

    return redirect(url_for("admin.users"))


def add_new_department(add_dep_form):
    new_department = Department(
        name = add_dep_form.name.data.strip()
    )
    db.session.add(new_department)
    db.session.commit()

    flash("Department Successfully Added")
    return redirect(url_for("admin.departments"))


def get_dep(dep_id):
    dep = Department.query.get(dep_id)
    if dep is None:
        flash("Something went wront: Could not find this department")
        return (True, redirect(url_for("admin.departments")))

    return (False, dep)


def edit_dep(editing_dep, edit_dep_form):
    new_name = edit_dep_form.name.data.strip()
    if new_name == editing_dep.name:
        flash("No changes made to this department")
        return redirect(url_for("admin.departments"))

    if Department.query.filter_by(name=new_name).first() is not None:
        flash("This department already exists")
        return redirect(url_for("admin.edit_department", department_id=editing_dep.id))

    editing_dep.name = new_name
    db.session.commit()

    flash("Department details successfully updated.")
    return redirect(url_for("admin.departments"))


def del_dep(dep_id):
    is_redirect, dep_to_delete = get_dep(dep_id)
    if is_redirect:
        return dep_to_delete

    else:
        db.session.delete(dep_to_delete)
        db.session.commit()
        flash("Department successfully deleted")
    
    return redirect(url_for("admin.departments"))

