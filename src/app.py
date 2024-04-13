import os
import json
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid
from extensions import db, login_manager
from routes.dashboard_pb import PolicyForm, ProfileForm

load_dotenv()
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

# connection_String = os.environ.get("AZURE_DATABASE_URL")
connection_String = os.environ.get("LOCAL_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_String

db.init_app(app)
login_manager.init_app(app)

users_data = {
    "username": "Emmie.MacGyver",
    "password": "NEhs5117NIVx0VF",
    "first_name": "Aubree",
    "surname": "O'Conner",
    "ID_number": 82865,
    "Address": "1004 Jakayla Plaza",
    "phone_number": "(506) 632-6488 x497",
    "profile_url": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/1071.jpg",
    "policies": [
        {
            "type": "Life Coverage",
            "coverage_amount": "608.89",
            "premium_amount": "93.18",
            "status": "Active",
        },
        {
            "type": "Car Coverage",
            "coverage_amount": "608.89",
            "premium_amount": "93.18",
            "status": "Pending",
        },
    ],
    "beneficiary": "Peter Orn",
    "id": "1",
}

policy_types = [
    "Vehicle Insurance",
    "Life Insurance",
    "Property Insurance",
    "Funeral Insurance",
]


@app.route("/")
def welcome_page():
    return render_template("Home.html", policies=policy_types)


# This will receive the user ID, so each user has their own information on the dashboard
@app.route("/dashboard")
def dashboard_page():
    user = current_user

    print(user.policies)  # this returns multiple policies
    return render_template(
        "dashboard.html", user=user.to_dict(), policies=user.policies
    )


@app.route("/get-quote")
def get_quote_page():
    return render_template("get-quote.html", policies=policy_types)


@app.route("/profile", methods=["POST", "GET"])
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

    print(policy_id)
    return render_template("policies.html", form=form, policy_id=policy_id)


from models.policy import Policy
from routes.form_bp import forms_bp

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
