import os
import json
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid
from calculator import car_quote, get_coverage
from extensions import db, login_manager
from models.vehicle import Vehicle
from models.policy import Policy
from models.users import User
from routes.dashboard_pb import PolicyForm, ProfileForm
from datetime import datetime, timedelta

load_dotenv()
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

# connection_String = os.environ.get("AZURE_DATABASE_URL")
connection_String = os.environ.get("LOCAL_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_String

db.init_app(app)
login_manager.init_app(app)


@app.route("/")
def welcome_page():
    return render_template("home.html")


# This will receive the user ID, so each user has their own information on the dashboard
@app.route("/dashboard")
@login_required
def dashboard_page():
    user = current_user

    # print(user.policies)  # this returns multiple policies
    return render_template(
        "dashboard.html", user=user.to_dict(), policies=user.policies
    )


@app.route("/get-quote")
@login_required
def get_quote_page():
    return render_template("get-quote.html")


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile_page():
    form = ProfileForm()
    # print("Yhooooo")
    if request.method == "POST":
        # Update user data here
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data

        try:
            db.session.commit()  # Commit the changes to the database
            flash("Profile updated successfully!", "profile_updated")
            return redirect(url_for("profile_page"))
        except Exception as e:
            db.session.rollback()
            flash(f"Profile update failed!: {e}", "profile_update_failed")
    elif request.method == "GET":
        # Pre-fill form with user's existing data
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.id_number.data = current_user.id_number
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email

    return render_template("profile.html", form=form, user=current_user)


@app.route("/policies", methods=["POST"])
@login_required
def policy_management():
    policy_id = request.form.get("policy_id")
    policy = Policy.query.get(policy_id)
    form = PolicyForm()

    # Pre-fill form with user's existing data
    form.car_type.data = policy.vehicle.car_type
    form.policy_type.data = policy.policy_type
    form.coverage_amount.data = policy.coverage_amount
    form.premium_amount.data = policy.premium_amount
    form.start_date.data = policy.start_date
    form.end_date.data = policy.end_date
    form.status.data = policy.status

    if form.validate_on_submit():
        # Update policy with new description
        policy.description = form.description.data
        # Save changes to the database
        # db.session.commit()
        flash("Policy updated successfully", "policy_updated")
        # flash("Policy update failed", "policy_update_failed")

    # print(policy_id)
    return render_template("policies.html", form=form, policy_id=policy_id)


@app.route("/quotes", methods=["GET", "POST"])
@login_required
def apply_policy():
    form = GetQuoteForm()
    if form.validate_on_submit():
        policy_type = form.policy_type.data
        age = form.age.data
        car_type = form.car_type.data
        year = form.year.data.year
        license_years = form.license_years.data
        accidents = form.accidents.data

        premium = car_quote(age, license_years, car_type, year, accidents)

        if request.form.get("button_apply") == "apply":
            # print("Greetings")
            try:
                # Calculate end date
                end_date = datetime.now().date() + timedelta(days=365)

                # For adding the vehicle
                vehicle = Vehicle(
                    user_id=current_user.id,
                    car_type=car_type,
                    year=year,
                    num_accidents=accidents,
                )
                db.session.add(vehicle)
                db.session.commit()

                vehicle_id = vehicle.vehicle_id

                # For adding the policy
                policy = Policy(
                    user_id=current_user.id,
                    policy_type=policy_type,
                    coverage_amount=get_coverage(premium),
                    premium_amount=premium,
                    start_date=datetime.now().date(),  # Convert to date object
                    end_date=end_date,
                    status="Pending",
                    vehicle_id=vehicle_id,
                )

                db.session.add(policy)
                db.session.commit()

                # Calculate the year when the license was issued
                license_issue_year = datetime.now().year - license_years
                license_issue_date = datetime(license_issue_year, 1, 1).date()
                current_user.license_year_issue = license_issue_date
                db.session.commit()

                flash(f"Successfully applied", "apply_message")
                return redirect(url_for("apply_policy"))
            except Exception as e:
                db.session.rollback()
                flash(f"Policy creation failed!: {e}", "policy_creation_failed")

        # return f"<h1> Quote: R{premium} </h1>"
        formatted_premium = "{:.2f}".format(premium)
        flash(f"Quote: R{formatted_premium}", "quote_message")
    return render_template("dashboard_quote.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome_page"))


from models.policy import Policy
from routes.form_bp import GetQuoteForm, forms_bp

app.register_blueprint(forms_bp, url_prefix="/form")

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.drop_all()
        db.create_all()  # This creates the table if it diesn't exist in the mssm database -> Sync tables to DB
        print("Creatiion done")
except Exception as e:
    print("Error connecting to the database:", e)
