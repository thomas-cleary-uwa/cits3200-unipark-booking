""" Routes used by auth blueprint

Authors: Thomas Cleary,
"""

from flask import render_template

from . import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html', title='login')
