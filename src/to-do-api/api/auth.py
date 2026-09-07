from flask import Flask, request, jsonify
import json

import db.connection as database


app = Flask(__name__)


@app.route("/register", methods=["POST"])
def create_account():
    """
    Return:
        error_message: account couldn't be created
        authentication_token: successful account creation
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if username is None or email is None or password is None:
        response = {"message": "missing information"}
        return jsonify(response), 400

    db_response = database.register_user(username, email, password)
    if db_response is None:
        response = {"message" : "username or email is arleady taken."}
        return jsonify(response), 409

    authentication_token = db_response
    return authentication_token, 201


@app.route("/login", methods=["POST"])
def login():
    """
    Returns:
        error_message: invalid login information
        authentication_token: successful login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        response = {"message": "missing information"}
        return jsonify(response), 400

    db_response = database.login(email, password)
    if db_response is None:
        response = {"message": "invalid email or password"}
        return jsonify(response), 401

    authentication_token = db_response
    return authentication_token, 200