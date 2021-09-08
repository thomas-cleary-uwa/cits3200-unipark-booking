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
            r'^\s*.*\s*$',
            message="regexp not met, change this msg"
        )
    ])

    password = PasswordField('Password:', validators=[
        DataRequired()
    ])

    submit = SubmitField('Log In')
