""" Admin only accessible routes

Authors: Thomas Cleary,
"""

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db

from ..helpers.decorators import admin_required
from . import admin


@admin.route("/add-user")
@login_required
@admin_required
def add_user():
    """ route for admin user to create new account """
    return render_template("admin/add_user.html")