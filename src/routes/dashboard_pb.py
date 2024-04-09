from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from extensions import db
from models.contactus import ContactUs
from models.users import User
from wtforms import (
    DateField,
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TelField,
    ValidationError,
    validators,
)
from wtforms.validators import InputRequired, Length, EqualTo
from wtforms import BooleanField
from flask_wtf import FlaskForm
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from calculator import car_quote, get_coverage


class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    name = StringField("Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    id_number = IntegerField("ID Number", validators=[InputRequired()])
    phone_number = TelField(
        "Phone Number",
        validators=[
            InputRequired(),
            validators.Regexp(
                "^\d+$", message="Phone number must contain only numbers"
            ),
        ],
    )
    email = EmailField("Email Address", validators=[InputRequired()])
    license_year_issue = DateField(
        "Year License Issued",
        default=datetime(datetime.now().year, 1, 1),
        validators=[InputRequired()],
    )
    submit = SubmitField("Update")

    def validate_username(self, field):
        # Informing WTF there's an error
        if field.data != current_user.username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError("Username already exists")
