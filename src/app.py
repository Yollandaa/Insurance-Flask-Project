import os
import json
from flask import Flask, jsonify, render_template, request
from flask_login import current_user
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid
from extensions import db, login_manager


load_dotenv()
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

connection_String = os.environ.get("AZURE_DATABASE_URL")
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
    return render_template("dashboard.html", data=user.to_dict())


@app.route("/get-quote")
def get_quote_page():
    return render_template("get-quote.html", policies=policy_types)


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
