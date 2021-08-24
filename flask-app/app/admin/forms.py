"""" forms for admin blueprint

Authors: Thomas Cleary,
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from ..models.user import User



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
    ])

    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(8, 64),
        EqualTo('password2', message="Passwords entered must match.")
    ])

    password2 = PasswordField('Cofirm Password: ', validators=[
        DataRequired()
    ])

    submit = SubmitField('Add User')


    # Methods of the form 'validate_<field-name>' will be called with previously
    # defined validators for <field-name>
    def validate_email(self, field):
        """ Raises an error if a user with field.data email already exists """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')