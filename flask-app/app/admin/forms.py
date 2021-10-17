"""" forms for admin blueprint

Authors: Thomas Cleary,
"""

import os
from dotenv import load_dotenv

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from ..models.user import User, Role, Department
from .. import create_app



class AddUserForm(FlaskForm):
    """ Form for admin user to create a new user """

    first_name = StringField('First Name: ', validators=[
        DataRequired(),
        Length(1, 64),
        ],
        render_kw={"placeholder" : "John"}
    )

    last_name = StringField('Last Name: ', validators=[
        DataRequired(),
        Length(1, 64),
        ],
        render_kw={"placeholder" : "Doe"}
    )
    
    email = StringField('Email: ', validators=[
        DataRequired(),
        Length(1, 64),
        Email()
        ],
        render_kw={"placeholder" : "firstname.lastname@uwa.edu.au"}
    )

    contact = StringField('Contact Number: ', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            r'^\s*[0-9]+\s*$',
            message='Contact number can only contain digits'
        )
        ],
        render_kw={"placeholder" : "0411222333"}
    )

    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(8, 64),
        EqualTo('password2', message="Passwords entered must match.")
    ])

    password2 = PasswordField('Cofirm Password: ', validators=[
        DataRequired()
    ])

    # department added as dynamic attribute
    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)

    submit = SubmitField('Add User')


    # Methods of the form 'validate_<field-name>' will be called with previously
    # defined validators for <field-name>
    def validate_email(self, field):
        """ Raises an error if a user with field.data email already exists """
        if User.query.filter_by(email=field.data.strip()).first():
            raise ValidationError('Email already registered.')



class EditUserForm(FlaskForm):
    """ Form for an admin user to edit a user's details """
    email = StringField('Email: ', validators=[
        DataRequired(),
        Length(1, 64),
        Email()
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
            r'^\s*[A-Z\sa-z]+\s*$',
            message="Name must only contain letters."
        )
    ])

    contact = StringField('Contact Number: ', validators=[
        DataRequired(),
        Length(1, 10),
        Regexp(
            r'^\s*[0-9]+\s*$',
            message='Contact number can only contain digits'
        )
        ],
       
    )

    # department added as dynamic attribute
    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)

    submit = SubmitField('Edit User')



class AddDepartmentForm(FlaskForm):
    """ form to add a department """

    name = StringField("Name: ", validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            r'^\s*[A-Z\sa-z]+\s*$',
            message="Department name must only contain [A-Za-z]"
        )

    ])

    submit = SubmitField('Add Department')

    def validate_name(self, field):
        """ report error if department with name already exists """
        if Department.query.filter_by(name=field.data.strip()).first():
            raise ValidationError("Department already exists")



class EditDepartmentForm(FlaskForm):
    """ Form to change department name """

    name = StringField("Name: ", validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            r'^\s*[A-Z\sa-z]+\s*$',
            message="Department name must only contain [A-Za-z]"
        )

    ])

    submit = SubmitField('Edit Department')