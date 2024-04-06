from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user
from extensions import db
from models.users import User
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo
from wtforms import BooleanField
from flask_wtf import FlaskForm
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


forms_bp = Blueprint("forms", __name__)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username/Email", validators=[InputRequired(), Length(min=6)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            Length(min=8),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    name = StringField("Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    id_number = StringField("ID Number", validators=[InputRequired()])
    phone_number = StringField("Phone Number", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired()])
    accept_terms = BooleanField(
        "I accept the terms and conditions", validators=[InputRequired()]
    )
    submit = SubmitField("Sign up")

    # This will be called automatically when the form is submitted
    # def validate_username(self, field):
    #     # Informing WTF there's an error
    #     user = User.query.filter_by(username=field.data).first()
    #     if user:
    #         raise ValidationError("Username already exists")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    # def validate_username(self, field):
    #     user = User.query.filter_by(username=field.data).first()
    #     if user is None:
    #         raise ValidationError("username does not exist")

    # Validate for login form
    # def validate_password(self, field):
    # user = User.query.filter_by(username=self.username.data).first()
    # if user:
    #     user_db_data = user.to_dict()
    #     form_password = field.data

    # Have to convert the password given to a hash and compare
    # if user_db_data["password"] != form_password:
    # First starts with the hash value password then the plaintext password
    # if not check_password_hash(user_db_data["password"], form_password):
    #     print(user_db_data["password"])
    #     raise ValidationError("Incorrect password")


class ContactForm(FlaskForm):
    name = StringField(label="Name", validators=[InputRequired(), Length(min=10)])
    phone_number = StringField(
        label="Phone Number", validators=[InputRequired(), Length(min=10)]
    )
    email = StringField(
        label="Email",
        validators=[
            InputRequired(),
        ],
    )
    message = StringField(label="Message")
    submit = SubmitField(label="Log In")


@forms_bp.route("/register", methods=["POST", "GET"])
def register():
    # GET and POST
    form = RegistrationForm()
    # ON POST
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # password_hash = generate_password_hash(password)
        # # print(password), generate_password_hash(password)
        # new_user = User(username=username, password=password_hash)
        # try:
        #     db.session.add(new_user)
        #     db.session.commit()
        #     return f"<h1> {username} Registration successful </h1>", 201
        # except Exception as e:
        #     db.session.rollback()
        #     return f"<h1> Registration Failed </h1>, {e}</h1>"

    # ONLY GET
    return render_template("register.html", form=form)


@forms_bp.route("/login", methods=["GET", "POST"])
def login():
    # GET and POST
    form = LoginForm()
    # ON POST
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # user = User.query.filter_by(username=username).first()
        # login_user(user)  # token is issued - (cookies) stored in the browser
        flash("Logged in successfully", "sucess")
        return "<h1>Successfully logged in</h1>"
        # return redirect(url_for("movies-list.get_movies"))

    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@forms_bp.route("/contact-us", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        print(
            f"Name:{form.name.data}, E-mail:{form.email.data}, message:{form.message.data}"
        )
    return render_template("home.html", form=form)
