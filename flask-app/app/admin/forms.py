"""" forms for admin blueprint

Authors: Thomas Cleary, Nur 'Iffah
"""

import os
from dotenv import load_dotenv

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from ..models.user import User, Role
from .. import create_app



class AddUserForm(FlaskForm):
    """ Form for admin user to create a new user """

    email = StringField('Email: ', validators=[
        DataRequired(),
        Length(1, 64),
        Email(),
        Regexp(
            r'^[A-Za-z]+\.[A-Za-z]+@uwa\.edu\.au$',
            message='Username must be an firstname.lastname@uwa.edu.au address'
        )
    ], render_kw={'placeholder': '12345678@uwa.edu.au'})

    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(8, 64)
    ])

    password2 = PasswordField('Cofirm Password: ', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords entered must match.")
    ])

    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)

    submit = SubmitField('Add User')


    # Methods of the form 'validate_<field-name>' will be called with previously
    # defined validators for <field-name>
    def validate_email(self, field):
        """ Raises an error if a user with field.data email already exists """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    