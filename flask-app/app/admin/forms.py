"""" forms for admin blueprint

Authors: Thomas Cleary,
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
        Regexp(
            r'^\s*[A-Za-z]+\.[A-Za-z]+@uwa\.edu\.au\s*$',
            message='Email must be an firstname.lastname@uwa.edu.au address'
        )
    ])

    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(8, 64),
        EqualTo('password2', message="Passwords entered must match.")
    ])

    password2 = PasswordField('Cofirm Password: ', validators=[
        DataRequired()
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



class EditUserForm(FlaskForm):
    """ Form for an admin user to edit a user's details """
    email = StringField('Email: ', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            r'^\s*[A-Za-z]+\.[A-Za-z]+@uwa\.edu\.au\s*$',
            message='Username must be an firstname.lastname@uwa.edu.au address'
        )
    ])

    first_name = StringField("First Name: ", validators=[
        DataRequired(),
        Regexp(
            r'^\s*[A-Za-z]+\s*$',
            message="Name must only contain letters."
        )
    ])

    last_name = StringField("Last Name: ", validators=[
        DataRequired(),
        Regexp(
            r'^\s*[A-Za-z]+\s*$',
            message="Name must only contain letters."
        )
    ])

    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)
