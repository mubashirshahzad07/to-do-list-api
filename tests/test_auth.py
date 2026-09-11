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
    assert "Authorization" in response.json
    assert response.json["Authorization"]


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

@pytest.fixture
def registered_user(client):
    data = {
        "username": "login_user",
        "email": "login_user_email",
        "password": "login_user_password",
    }

    client.post("/register", data=data)

    return data


def test_login_success(client, registered_user):
    response = client.post(
        "/login",
        data={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    assert "Authorization" in response.json
    assert response.json["Authorization"]


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
