import pytest


# ---------- Registration ----------

def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "username": "new_user",
            "email": "new_user_email",
            "password": "new_user_password",
        },
    )

    assert response.status_code == 201
    assert "access_token" in response.json
    assert response.json["access_token"]


def test_register_duplicate_username(client):
    data = {
        "username": "new_user",
        "email": "new_user_email",
        "password": "new_user_password",
    }

    client.post("/register", data=data)

    response = client.post(
        "/register",
        data={
            "username": "new_user",
            "email": "different_email",
            "password": "new_user_password",
        },
    )

    assert response.status_code == 409
    assert response.json == {
        "message": "username or email is already taken."
    }


def test_register_duplicate_email(client):
    data = {
        "username": "new_user",
        "email": "new_user_email",
        "password": "new_user_password",
    }

    client.post("/register", data=data)

    response = client.post(
        "/register",
        data={
            "username": "different_username",
            "email": "new_user_email",
            "password": "new_user_password",
        },
    )

    assert response.status_code == 409
    assert response.json == {
        "message": "username or email is already taken."
    }


@pytest.mark.parametrize(
    "data",
    [
        {
            "email": "new_user_email",
            "password": "new_user_password",
        },
        {
            "username": "",
            "email": "new_user_email",
            "password": "new_user_password",
        },
        {
            "username": "new_user",
            "password": "new_user_password",
        },
        {
            "username": "new_user",
            "email": "",
            "password": "new_user_password",
        },
        {
            "username": "new_user",
            "email": "new_user_email",
        },
        {
            "username": "new_user",
            "email": "new_user_email",
            "password": "",
        },
    ],
)
def test_register_missing_information(client, data):
    response = client.post("/register", data=data)

    assert response.status_code == 400
    assert response.json == {
        "message": "missing information"
    }


# ---------- Login ----------

def test_login_success(client, registered_user):
    response = client.post(
        "/login",
        data={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert response.json["access_token"]


@pytest.mark.parametrize(
    "data",
    [
        {
            "password": "login_user_password",
        },
        {
            "email": "",
            "password": "login_user_password",
        },
        {
            "email": "login_user_email",
            "password": "",
        },
    ],
)
def test_login_missing_information(client, data):
    response = client.post("/login", data=data)

    assert response.status_code == 400
    assert response.json == {
        "message": "missing information"
    }


def test_login_invalid_email(client, registered_user):
    response = client.post(
        "/login",
        data={
            "email": "invalid_email",
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 401
    assert response.json == {
        "message": "invalid email or password"
    }


def test_login_invalid_password(client, registered_user):
    response = client.post(
        "/login",
        data={
            "email": registered_user["email"],
            "password": "invalid_password",
        },
    )

    assert response.status_code == 401
    assert response.json == {
        "message": "invalid email or password"
    }


# --------------- REFRESH TOKEN -------------

def test_successful_refresh_token(client):
    register_repsonse = client.post(
        "/register",
        data={
            "username": "refresh_username_1",
            "email": "refresh_email_1",
            "password": "refresh_password"
        }
    )

    assert register_repsonse.status_code == 201

    refresh_token = register_repsonse.json.get("refresh_token")

    response = client.post(
        "/refresh",
        headers={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_missing_information_refresh_token(client):
    response = client.post("/refresh")

    assert response.status_code == 400
    assert response.json["message"] == "missing information"


def test_invalid_refresh_token(client):
    response = client.post(
        "/refresh",
        headers={
            "refresh_token": "invalid_refresh_token"
        }
    )

    assert response.status_code == 401
    assert response.json["message"] == "unauthenticated"
