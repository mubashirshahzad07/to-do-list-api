from flask import Blueprint, request, jsonify

import db.connection as database


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
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

    token = database.register_user(username, email, password)
    if token is None:
        response = {"message" : "username or email is arleady taken."}
        return jsonify(response), 409

    return jsonify(token), 201


@auth.route("/login", methods=["POST"])
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

    token = database.login(email, password)
    if token is None:
        response = {"message": "invalid email or password"}
        return jsonify(response), 401

    return jsonify(token), 200