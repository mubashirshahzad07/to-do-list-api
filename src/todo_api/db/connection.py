import sqlite3
import jwt
import os

from hashlib import sha256
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

from ..db import queries


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise KeyError("SECRET_KEY does not exist.")

connection = sqlite3.connect("todo.db")

connection.execute("PRAGMA foreign_keys = ON")
connection.execute(queries.create_users_table)
connection.execute(queries.create_todos_table)

connection.commit()
connection.close()


def register_user(username: str, email: str, password: str) -> dict | None:
    """
    Return:
        None: username or email is already taken
        dict (access_token, refresh_token): user is created
    """

    connection = sqlite3.connect("todo.db")

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

    access_payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }

    refresh_payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=30)
    }

    access_token = jwt.encode(
        access_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        refresh_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return response


def login(email: str, password: str) -> dict | None:
    """
    Return:
        None: invalid login information
        dict (access_token, refresh_token): valid login information
    """

    connection = sqlite3.connect("todo.db")

    cursor = connection.execute(queries.find_user_with_email, (email, ))
    user = cursor.fetchone()
    connection.close()

    if not user:
        return None

    user_id, password_hash = user[0], user[1]
    entered_hash = sha256(password.encode("utf-8")).hexdigest()

    if entered_hash != password_hash:
        return None

    access_payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }

    refresh_payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=30)
    }

    access_token = jwt.encode(
        access_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        refresh_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return response


def _verify_access_token(access_token: str) -> dict | None:
    """
    Return:
        None: unauthenticated
        dict (payload): valid token
    """
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        return None

    if payload.get("type") != "access":
        return None

    return payload


def _verify_refresh_token(access_token: str) -> dict | None:
    """
    Return:
        None: unauthenticated
        dict (payload): valid token
    """
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload


def create_to_do_item(access_token: str, title: str, desc: str) -> dict | None:
    """
    Return:
        None: unauthenticated or unauthorized
        dict (created_item): successful creation of to do item
    """

    payload = _verify_access_token(access_token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

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
        access_token: str,
        todo_id: int,
        title: str,
        desc: str
) -> dict | None:
    """
    Return:
        None: Unauthenticated or Unauthorized
        dict(updated_item): todo item is successfully updated
    """

    payload = _verify_access_token(access_token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

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


def delete_todo_item(access_token: str, todo_id: int) -> int | None:
    """
    Return:
        None: unauthenticated, unauthorized, or todo item doesn't exist
        int(status_code): successful deletion
    """

    payload = _verify_access_token(access_token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

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


def get_todo_items(access_token: str, page: int, limit: int) -> dict | None:
    """
    Return:
        None: unauthenticated
        dict(todo_items): successful retreival
    """

    payload = _verify_access_token(access_token)
    if payload is None:
        return None

    user_id = payload.get("user_id")
    if user_id is None:
        return None

    connection = sqlite3.connect("todo.db")

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


def refresh_access_token(refresh_token: str) -> dict | None:
    """
    Returns:
        None: invalid refresh token
        dict (new_access_token, same_refresh_token): valid refresh token
    """

    payload = _verify_refresh_token(refresh_token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    access_payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }

    access_token = jwt.encode(
        access_payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    return response
