import json
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

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


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # To do: Need to uathenticate login
        return redirect(url_for("dashboard_page"))
    return render_template("login.html")


@app.route("/sign-up")
def signup_page():
    return render_template("sign-up.html")


# This will receive the user ID, so each user has their own information on the dashboard
@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html", data=users_data)


@app.route("/get-quote")
def get_quote_page():
    return render_template("get-quote.html", policies=policy_types)
