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
    assert "Authorization" in register_response.json

    Authorization = register_response.json["Authorization"]

    response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers={
            "Authorization": Authorization
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
            "Authorization": "invalid_Authorization"
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
                "Authorization": ""
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
                "Authorization": "doesntmatter"
            }

       ),
       (
            {
                "description": "desc of something"
            },
            {
                "Authorization": "doesntmatter"
            }

       ),
       (
            {
                "title": "do something",
                "description": ""
            },
            {
                "Authorization": "doesntmatter"
            }

       ),

       (
            {
                "title": "do something",
            },
            {
                "Authorization": "doesntmatter"
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


# ------------ UPDATE TO DO ITEM ----------

def test_successful_item_update(client):
    register_response = client.post(
        "/register",
        data={
            "username": "update_username_1",
            "email": "update_email_1",
            "password": "update_password"
        }
    )

    assert register_response.status_code == 201

    Authorization = register_response.json["Authorization"]
    headers = {
        "Authorization": Authorization
    }

    create_item_response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers=headers
    )

    assert create_item_response.status_code == 201

    todo_id = create_item_response.json["id"]

    new_title = "new title"
    new_description = "new description"

    response = client.put(
        f"/todos/{todo_id}",
        data={
            "title": new_title,
            "description": new_description
        },
        headers=headers
    )

    assert response.status_code == 200
    assert "index" in response.json
    assert response.json["id"] == todo_id
    assert response.json["title"] == new_title
    assert response.json["description"] == new_description


def test_unauthorized_item_update(client):
    register_response_1 = client.post(
        "/register",
        data={
            "username": "udpate_username_2",
            "email": "update_email_2",
            "password": "update_password"
        }
    )

    assert register_response_1.status_code == 201
    Authorization1 = register_response_1.json["Authorization"]

    register_response_2 = client.post(
        "/register",
        data={
            "username": "udpate_username_3",
            "email": "update_email_3",
            "password": "update_password"
        }
    )

    assert register_response_2.status_code == 201
    Authorization2 = register_response_2.json["Authorization"]

    create_item_response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers={
            "Authorization": Authorization1
        }
    )

    assert create_item_response.status_code == 201

    todo_id = create_item_response.json["id"]

    new_title = "new title"
    new_description = "new description"

    response = client.put(
        f"/todos/{todo_id}",
        data={
            "title": new_title,
            "description": new_description
        },
        headers={
            "Authorization": Authorization2
        }
    )

    expected_response = {"message": "Forbidden"}

    assert response.status_code == 403
    assert response.json == expected_response


@pytest.mark.parametrize(
    "data, headers",
    [
        (
            {
                "title": "some title",
                "description": "some desc"
            },
            {
                "Authorization": ""
            }
        ),
        (
            {
                "title": "some title",
                "description": "some desc"
            },
            {}
        ),
        (
            {
                "title": "",
                "description": "some desc"
            },
            {
                "Authorization": "does not matter"
            }
        ),
        (
            {
                "description": "some desc"
            },
            {
                "Authorization": "does not matter"
            }
        ),
        (
            {
                "title": "some title",
                "description": ""
            },
            {
                "Authorization": "does not matter"
            }
        ),
        (
            {
                "title": "some title",
            },
            {
                "Authorization": "does not matter"
            }
        ),
    ]
)
def test_missing_information_item_update(client, data, headers):
    response = client.put(
        "/todos/1",
        data=data,
        headers=headers
    )

    expected_response = {"message": "missing information"}

    assert response.status_code == 400
    assert response.json == expected_response


# ------------ DELETE TO DO ITEM ----------

def test_successful_item_deletion(client):
    register_response = client.post(
        "/register",
        data={
            "username": "delete_username_1",
            "email": "delete_email_1",
            "password": "delete_password"
        }
    )

    assert register_response.status_code == 201

    Authorization = register_response.json["Authorization"]
    headers = {
        "Authorization": Authorization
    }

    create_item_response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers=headers
    )

    assert create_item_response.status_code == 201

    todo_id = create_item_response.json["id"]

    response = client.delete(
        f"/todos/{todo_id}",
        headers=headers
    )

    assert response.status_code == 204
    assert response.data == b""


def test_unauthenticated_item_deletion(client):
    response = client.delete(
        "/todos/1"
    )

    expected_response = {
        "message": "Unauthenticated"
    }

    assert response.status_code == 401
    assert response.json == expected_response


def test_unauthorized_item_deletion(client):
    register_response_1 = client.post(
        "/register",
        data={
            "username": "delete_username_2",
            "email": "delete_email_2",
            "password": "delete_password"
        }
    )

    assert register_response_1.status_code == 201
    Authorization1 = register_response_1.json["Authorization"]

    register_response_2 = client.post(
        "/register",
        data={
            "username": "delete_username_3",
            "email": "delete_email_3",
            "password": "delete_password"
        }
    )

    assert register_response_2.status_code == 201
    Authorization2 = register_response_2.json["Authorization"]

    create_item_response = client.post(
        "/todos",
        data={
            "title": "do something",
            "description": "desc of something"
        },
        headers={
            "Authorization": Authorization1
        }
    )

    assert create_item_response.status_code == 201

    todo_id = create_item_response.json["id"]

    response = client.delete(
        f"/todos/{todo_id}",
        headers={
            "Authorization": Authorization2
        }
    )

    expected_response = {
        "message": "Forbidden"
    }

    assert response.status_code == 403
    assert response.json == expected_response


# ------------ GET TO DO ITEMS ----------

def test_successful_item_retrieval(client):
    register_response = client.post(
        "/register",
        data={
            "username": "get_username_1",
            "email": "get_email_1",
            "password": "get_password"
        }
    )

    assert register_response.status_code == 201

    Authorization = register_response.json["Authorization"]
    headers = {
        "Authorization": Authorization
    }

    first_item_response = client.post(
        "/todos",
        data={
            "title": "first todo",
            "description": "first description"
        },
        headers=headers
    )

    assert first_item_response.status_code == 201

    second_item_response = client.post(
        "/todos",
        data={
            "title": "second todo",
            "description": "second description"
        },
        headers=headers
    )

    assert second_item_response.status_code == 201

    page = 1
    limit = 10

    response = client.get(
        "/todos",
        query_string={
            "page": page,
            "limit": limit
        },
        headers=headers
    )

    expected_total = 2

    assert response.status_code == 200
    assert len(response.json["data"]) == 2

    assert response.json["data"][0]["title"] == "first todo"
    assert response.json["data"][0]["description"] == "first description"

    assert response.json["data"][1]["title"] == "second todo"
    assert response.json["data"][1]["description"] == "second description"

    assert response.json["page"] == page
    assert response.json["limit"] == limit
    assert response.json["total"] == expected_total


@pytest.mark.parametrize(
    "query_string, headers",
    [
        (
            {
                "page": 1,
                "limit": 10
            },
            {}
        ),
        (
            {
                "page": 1,
                "limit": 10
            },
            {
                "Authorization": ""
            }
        ),
        (
            {
                "limit": 10
            },
            {
                "Authorization": "doesntmatter"
            }
        ),
        (
            {
                "page": 1
            },
            {
                "Authorization": "doesntmatter"
            }
        ),
        (
            {},
            {
                "Authorization": "doesntmatter"
            }
        ),
        (
            {
                "page": 0,
                "limit": 10
            },
            {
                "Authorization": "doesntmatter"
            }
        ),
        (
            {
                "page": 1,
                "limit": 0
            },
            {
                "Authorization": "doesntmatter"
            }
        )
    ]
)
def test_missing_information_item_retrieval(
    client,
    query_string,
    headers
):
    response = client.get(
        "/todos",
        query_string=query_string,
        headers=headers
    )

    expected_response = {
        "message": "missing information"
    }

    assert response.status_code == 400
    assert response.json == expected_response


def test_unauthenticated_item_retrieval(client):
    register_response = client.post(
        "/register",
        data={
            "username": "get_username_2",
            "email": "get_email_2",
            "password": "get_password"
        }
    )

    assert register_response.status_code == 201

    Authorization = register_response.json["Authorization"]

    response = client.get(
        "/todos",
        query_string={
            "page": 1,
            "limit": 10
        },
        headers={
            "Authorization": "invalid_Authorization"
        }
    )

    expected_response = {
        "message": "Unauthenticated"
    }

    assert response.status_code == 401
    assert response.json == expected_response
