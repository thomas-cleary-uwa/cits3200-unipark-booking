""" Routes used by main blueprint
    
    Authors: Thomas Cleary, 
"""

from flask import render_template

from . import main


@main.route('/')
@main.route('/index')
def index():
    """ initial route for the application """
    return render_template('main/index.html', title='index')
