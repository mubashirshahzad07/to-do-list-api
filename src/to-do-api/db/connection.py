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

    # creates users table
    connection.execute(queries.create_users_table)

    # creates todos table
    connection.execute(queries.create_todos_table)

    connection.commit()


def create_user(username: str, email: str, password: str) -> str | None:
    """
    Return:
        None: username or email is already taken
        token(str): new account is created
    """

    connection = sqlite3.connect("todo.db")

    create_tables(connection)

    cursor = connection.execute(queries.find_username_or_email, (username, email))
    exists = cursor.fetchone()
    if exists:
        connection.close()
        return None

    password_hash = sha256(password.encode("utf-8")).hexdigest()
    cursor = connection.execute(queries.add_user, (username, email, password_hash))

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    token = jwt.encode(
        {"user_id": user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def login(email: str, password: str) -> str | None:
    """ 
    Return:
        None: invalid login information
        token(str): valid login information
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
        return token

    connection.close()
    return None