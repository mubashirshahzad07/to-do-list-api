from flask import Blueprint, request, jsonify

import db.connection as database


todo = Blueprint("todo", __name__)


@todo.route("/todos", methods=["POST"])
def create_todo_item():
    """
    Returns:
        400: missing information
        401: unauthenticated
        201: todo item successfully created
    """

    token = request.headers.get("token")
    title = request.form.get("title")
    description = request.form.get("description")

    if not token or not title or not description:
        response = {"message": "missing information"}
        return jsonify(response), 400

    item_created = database.create_to_do_item(token, title, description)

    if item_created is None:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    return jsonify(item_created), 201


@todo.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo_item(todo_id: int):
    """
    Returns:
        400: missing information
        401: unauthorized
        200: successful update
    """

    token = request.headers.get("token")
    title = request.form.get("title")
    description = request.form.get("description")

    if not token or not title or not description:
        response = {"message": "missing information"}
        return jsonify(response), 400

    updated_item = database.update_to_do_item(
        token,
        todo_id,
        title,
        description
    )
    if updated_item is None:
        response = {"message": "Unauthorized"}
        return jsonify(response), 401

    return jsonify(updated_item), 200


@todo.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_item(todo_id):
    """
    Returns:
        401: unauthenticated
        403: forbidden / unauthorized
        204: successful deletion
    """

    token = request.headers.get("token")

    if not token:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    deleted_item = database.delete_todo_item(token, todo_id)
    if deleted_item is None:
        response = {"message": "Forbidden"}
        return jsonify(response), 403

    return "", 204


@todo.route("/todos", methods=["GET"])
def get_todo_items():
    """
    Returns:
        400: missing information
        401: unauthenticated
        200: successful retreival
    """

    token = request.headers.get("token")
    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)

    if not token or not page or not limit:
        response = {"message": "missing information"}
        return jsonify(response), 400

    todo_items = database.get_todo_items(token, page, limit)
    if todo_items is None:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    return jsonify(todo_items), 200