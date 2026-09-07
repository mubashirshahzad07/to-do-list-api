from hashlib import sha256
from dotenv import load_dotenv

import sqlite3
import jwt
import os

import queries


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise KeyError("SECRET_KEY does not exist.")


def create_tables(connection: sqlite3.Connection) -> None:
    # enable foreign keys
    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute(queries.create_users_table)
    connection.execute(queries.create_todos_table)

    connection.commit()


def register_user(username: str, email: str, password: str) -> dict | None:
    """
    Return:
        None: username or email is already taken
        dict (token): user is created
    """

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(
        queries.find_username_or_email,
        (username, email)
    )
    exists = cursor.fetchone()
    if exists:
        connection.close()
        return None

    password_hash = sha256(password.encode("utf-8")).hexdigest()
    cursor = connection.execute(
        queries.add_user,
        (username, email, password_hash)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    token = jwt.encode(
        {"user_id": user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token}


def login(email: str, password: str) -> dict | None:
    """
    Return:
        None: invalid login information
        dict (token): valid login information
    """

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(queries.find_user_with_email, (email, ))
    user = cursor.fetchone()
    if not user:
        connection.close()
        return None

    user_id, password_hash = user[0], user[1]
    entered_hash = sha256(password.encode("utf-8")).hexdigest()

    if entered_hash == password_hash:
        token = jwt.encode(
            {"user_id": user_id},
            SECRET_KEY,
            algorithm="HS256"
        )

        connection.close()
        return {"token": token}

    connection.close()
    return None


def _verify_token(token: str) -> dict | None:
    """
    Return:
        None: unauthenticated
        dict (payload): valid token
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        return None

    return payload


def create_to_do_item(token: str, title: str, desc: str) -> dict | None:
    """
    Return:
        None: unauthenticated or unauthorized
        dict (created_item): successful creation of to do item
    """

    payload = _verify_token(token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(queries.add_todo_item, (user_id, title, desc))
    connection.commit()

    todo_id = cursor.lastrowid

    cursor = connection.execute(queries.get_todo_items_count, (user_id, ))
    index = cursor.fetchone()[0]

    connection.close()

    response = {
        "index": index,
        "id": todo_id,
        "title": title,
        "description": desc
    }

    return response


def update_to_do_item(
        token: str,
        todo_id: int,
        title: str,
        desc: str
) -> dict | None:
    """
    Return:
        None: Unauthenticated or Unauthorized
        dict(updated_item): todo item is successfully updated
    """

    payload = _verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(
        queries.update_todo_item,
        (title, desc, todo_id, user_id)
    )
    connection.commit()

    rows_affected = cursor.rowcount
    if rows_affected == 0:
        connection.close()
        return None

    cursor = connection.execute(
        queries.get_updated_todo_item_index,
        (user_id, todo_id)
    )
    index = cursor.fetchone()[0]

    connection.close()

    response = {
        "index": index,
        "id": todo_id,
        "title": title,
        "description": desc
    }

    return response


def delete_todo_item(token: str, todo_id: int) -> int | None:
    """
    Return:
        None: unauthenticated, unauthorized, or todo item doesn't exist
        int(status_code): successful deletion
    """

    payload = _verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(
        queries.delete_todo_item,
        (todo_id, user_id)
    )
    connection.commit()

    rows_affected = cursor.rowcount

    if rows_affected == 0:
        connection.close()
        return None

    connection.close()

    return 204


def get_todo_items(token: str, page: int, limit: int) -> dict | None:
    """
    Return:
        None: unauthenticated
        dict(todo_items): successful retreival
    """

    payload = _verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    offset = (page - 1) * limit
    cursor = connection.execute(
        queries.get_todo_items_paginated,
        (user_id, limit, offset)
    )
    rows = cursor.fetchall()

    cursor = connection.execute(
        queries.get_total_todos_for_user_id,
        (user_id, )
    )
    total = cursor.fetchone()[0]

    connection.close()

    data = []
    for index, (todo_id, title, desc) in enumerate(rows, start=1):
        curr_data = {
            "index": index,
            "id": todo_id,
            "title": title,
            "description": desc
        }
        data.append(curr_data)

    response = {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total
    }

    return response
