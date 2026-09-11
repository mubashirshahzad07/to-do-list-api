import pytest

from src.todo_api import create_app


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


@pytest.fixture
def registered_user(client):
    data = {
        "username": "login_user",
        "email": "login_user_email",
        "password": "login_user_password",
    }

    client.post("/register", data=data)

    return data
