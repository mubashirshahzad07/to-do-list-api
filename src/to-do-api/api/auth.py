from flask import Flask, request, jsonify
import json

import db.connection as database


app = Flask(__name__)


@app.route("/register", methods=["POST"])
def create_account():
    """
    Returns:
        400: missing information
        409: username or email already taken
        201: account successfully created
    """

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        response = {"message": "missing information"}
        return jsonify(response), 400

    db_response = database.register_user(username, email, password)
    if db_response is None:
        response = {"message" : "username or email is arleady taken."}
        return jsonify(response), 409

    return jsonify(db_response), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Returns:
        400: missing information
        401: invalid email or password
        200: successful login
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        response = {"message": "missing information"}
        return jsonify(response), 400

    db_response = database.login(email, password)
    if db_response is None:
        response = {"message": "invalid email or password"}
        return jsonify(response), 401

    return jsonify(db_response), 200