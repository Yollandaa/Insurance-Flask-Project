import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def welcome_page():
    return render_template("Home.html")


@app.route("/login")
def login_page():
    return render_template("login.html")
