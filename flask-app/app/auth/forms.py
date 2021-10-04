""" forms for user authentication 

Authors: Thomas Cleary,
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo



class LoginForm(FlaskForm):
    """ Login form for existing users """
    email = StringField('Staff Email:', validators=[
        DataRequired(),
        Length(1, 64),
        Email()
    ])

    password = PasswordField('Password:', validators=[
        DataRequired()
    ])

    submit = SubmitField('Log In')

class EditProfileForm(FlaskForm):
    """ Form for an user to edit profile """

    # department added as dynamic attribute
    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)

    first_name = StringField('First Name: ', validators=[
        ],
        render_kw={"disabled" : "disabled"}
    )

    last_name = StringField('Last Name: ', validators=[
        ],
        render_kw={"disabled" : "disabled"}
    )
    
    email = StringField('Email: ', validators=[
        ],
        render_kw={"disabled" : "disabled"}
    )

    # department added as dynamic attribute
    # role added as dyanmic attribute 
    # (when using this form us setattr() to add a SelectField attribute to this class)

    submit = SubmitField('Edit User')


class ChangePasswordForm(FlaskForm):
    """ Form for an user to change password """


    password = PasswordField('Password: ', validators=[
        DataRequired(),
        Length(8, 64),
    ])

    submit = SubmitField('Edit User')
