""" Forms for Bookings  blueprint 

Authors: Thomas Cleary,
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class ConfirmBookingForm(FlaskForm):
    """ Form to confirm a booking """

    title = SelectField("Title: ", choices=[
        'Assoc. Prof.', 'Dean', 'Dr.',
        'Gov.', 'Hon.', 'Master',
        'Mayor', 'Mayoress', 'Miss',
        'Mr.', 'Mrs', 'Ms', 'Mx',
        'Prof.', 'Sen.', 'Sir'
    ])

    guest_first_name = StringField("Guest First Name: ", validators=[
        DataRequired(),
        Length(1, 28)
    ])

    guest_last_name = StringField("Guest Last Name: ", validators=[
        DataRequired(),
        Length(1, 28)
    ])

    vehicle_rego = StringField("Vehicle Registration: ", validators=[
        Length(0, 16),
    ])

    ts_and_cs = BooleanField("I have read, and accept the terms and conditions.")





