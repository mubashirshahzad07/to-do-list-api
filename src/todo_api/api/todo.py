from flask import Blueprint, request, jsonify

from ..db import connection as database


todo = Blueprint("todo", __name__)


@todo.route("/todos", methods=["POST"])
def create_todo_item():
    """
    Returns:
        400: missing information
        401: unauthenticated
        201: todo item successfully created
    """

    authorization = request.headers.get("Authorization")
    title = request.form.get("title")
    description = request.form.get("description")

    if not authorization or not title or not description:
        response = {"message": "missing information"}
        return jsonify(response), 400

    item_created = database.create_to_do_item(authorization, title, description)

    if item_created is None:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    return jsonify(item_created), 201


@todo.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo_item(todo_id: int):
    """
    Returns:
        400: missing information
        403: forbidden
        200: successful update
    """

    authorization = request.headers.get("Authorization")
    title = request.form.get("title")
    description = request.form.get("description")

    if not authorization or not title or not description:
        response = {"message": "missing information"}
        return jsonify(response), 400

    updated_item = database.update_to_do_item(
        authorization,
        todo_id,
        title,
        description
    )
    if updated_item is None:
        response = {"message": "Forbidden"}
        return jsonify(response), 403

    return jsonify(updated_item), 200


@todo.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_item(todo_id):
    """
    Returns:
        401: unauthenticated
        403: forbidden / unauthorized
        204: successful deletion
    """

    authorization = request.headers.get("Authorization")

    if not authorization:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    deleted_item = database.delete_todo_item(authorization, todo_id)
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

    authorization = request.headers.get("Authorization")
    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)

    if not authorization or not page or not limit or page <= 0 or limit <= 0:
        response = {"message": "missing information"}
        return jsonify(response), 400

    todo_items = database.get_todo_items(authorization, page, limit)
    if todo_items is None:
        response = {"message": "Unauthenticated"}
        return jsonify(response), 401

    return jsonify(todo_items), 200
