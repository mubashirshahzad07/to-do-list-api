import pytest


# ------- CREATE TO DO ITEM ----------

def test_successful_item_creation(client):
    register_response = client.post(
        "/register",
        data={
            "username": "create_username_1",
            "email": "create_email_1",
            "password": "create_password"
        }
    )

    assert register_response.status_code == 201
    assert "token" in register_response.json

    token = register_response.json["token"]

    response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers={
            "token": token
        }
    )

    expected_response = {
        "index": 1,
        "id": 1,
        "title": "do something",
        "description": "desc of something"
    }

    assert response.status_code == 201
    assert response.json == expected_response


def test_unauthenticated_item_creation(client):
    response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        }, 
        headers={
            "token": "invalid_token"
        }
    )

    expected_response = {"message": "Unauthenticated"}

    assert response.status_code == 401
    assert response.json == expected_response


@pytest.mark.parametrize(
    "data, headers",
    [
       (
            {
                "title": "do something",
                "description": "desc of something"
            },
            {
                "token": ""
            }
       ),
       (
            {
                "title": "do something",
                "description": "desc of something"
            },
            {
            }

       ),
       (
            {
                "title": "",
                "description": "desc of something"
            },
            {
                "token": "doesntmatter"
            }

       ),
       (
            {
                "description": "desc of something"
            },
            {
                "token": "doesntmatter"
            }

       ),
       (
            {
                "title": "do something",
                "description": ""
            },
            {
                "token": "doesntmatter"
            }

       ),
       
       (
            {
                "title": "do something",
            },
            {
                "token": "doesntmatter"
            }

       )
    ]
)
def test_missing_information_item_creation(client, data, headers):
    response = client.post(
        "/todos",
        data=data,
        headers=headers
    )

    expected_response = {
        "message": "missing information"
    }

    assert response.status_code == 400
    assert response.json == expected_response