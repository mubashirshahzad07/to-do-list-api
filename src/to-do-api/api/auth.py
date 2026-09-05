from flask import Flask, request
import json


app = Flask(__name__)


@app.route("/register", methods=["POST"])
def create_account():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        response = {"message": "missing information"}
        return json.dumps(response)

    return ""


@app.route("/login", methods=["POST"])
def login():
    return {}