""" forms for user authentication 

Authors: Thomas Cleary,
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp



class LoginForm(FlaskForm):
    """ Login form for existing users """
    email = StringField('Staff Email:', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            r'^\s*[A-Za-z]+\.[A-Za-z]+@uwa\.edu\.au\s*$',
            message='Email must be an firstname.lastname@uwa.edu.au address'
        )
    ])

    password = PasswordField('Password:', validators=[
        DataRequired()
    ])

    submit = SubmitField('Log In')
