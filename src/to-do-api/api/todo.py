from flask import  Blueprint, request, jsonify

import db.connection as database


todo = Blueprint("todo", __name__)


@todo.route("/todos", methods=["POST"])
def create_todo_item():
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


@todo.route("/todos/<int:todo_id>", methdos=["PUT"])
def update_todo_item(todo_id: int):
    token = request.headers.get("token")
    title = request.form.get("title")
    description = request.form.get("description")

    if not token or not title or not description:
        response = {"message": "missing information"}
        return jsonify(response), 400

    updated_item = database.update_to_do_item(token, todo_id, title, description)
    if updated_item is None:
        response = {"message": "Unauthorized"}
        return jsonify(response), 401

    return jsonify(updated_item), 200


@todo.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_item(todo_id):
    token = request.headers.get("token")


    return {}


@todo.route("/todos", methods=["GET"])
def get_todo_items():
    return {}