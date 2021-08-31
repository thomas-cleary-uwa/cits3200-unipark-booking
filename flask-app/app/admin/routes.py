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
    all_users = User.query.join(Role, User.role_id==Role.id)
    admin_users = all_users.filter(Role.name=="admin")
    normal_users = all_users.filter(Role.name=="user")
    disabled_users = all_users.filter(Role.name=="disabled")
    return render_template(
        "admin/users.html", 
        admin_users=admin_users, 
        normal_users=normal_users,
        disabled_users=disabled_users)


@admin.route("/add-user", methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """ route for admin user to create new account """

    role = SelectField("Role: ", choices=Role.get_role_names())
    setattr(AddUserForm, 'role', role)
    add_user_form = AddUserForm()

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

    add_user_form.role.default = "user"
    add_user_form.process() # need to cal this to set new default
    
    return render_template('admin/add_user.html', add_user_form=add_user_form)


# NOTE: probably change the route <int:id> to be a different slug
# NOTE: Probably want to add reset password functionality at some point
@admin.route("/edit-user/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """ provide a form to edit / delete the user with id = id """
    role = SelectField("Role: ", choices=Role.get_role_names())
    setattr(EditUserForm, 'role', role)

    edit_user_form = EditUserForm()

    editing_user = User.query.get(user_id)
    if editing_user is None:
        flash("Something went wrong: Could not find this user")
        return redirect(url_for("admin.users"))

    if edit_user_form.validate_on_submit():
        # check if email exists in database and is not the same as editing user
        entered_email = edit_user_form.email.data.strip()

        # if the admin user is editing themself
        if current_user == editing_user:
            if edit_user_form.role.data != "admin":
                flash("You cannot change your own role")
                return redirect(url_for("admin.edit_user", user_id=user_id))


        email_check_user = User.query.filter_by(email=entered_email).first()
        if email_check_user is not None and email_check_user.id != editing_user.id:
            flash("The entered email address is already in use.")
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        editing_user.email = entered_email
        editing_user.first_name = edit_user_form.first_name.data.strip().capitalize()
        editing_user.last_name = edit_user_form.last_name.data.strip().capitalize()
        editing_user.role_id = Role.query.filter_by(name=edit_user_form.role.data).first().id

        db.session.commit()

        flash("User Details Successfully Updated.")
        return redirect(url_for('admin.users'))

    edit_user_form.email.default = editing_user.email
    edit_user_form.first_name.default = editing_user.first_name
    edit_user_form.last_name.default = editing_user.last_name
    edit_user_form.role.default = editing_user.role.name
    edit_user_form.process() # need to call this to actually set new default values
    
    return render_template(
        "admin/edit_user.html", 
        edit_user_form=edit_user_form,
        editing_user=editing_user)


@admin.route("/delete-user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    """ route to perform deletion of user from db """

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