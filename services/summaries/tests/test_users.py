# project/tests/test_users.py


import json
import pdb


def test_create_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "Jane Doe"})
    )
    assert response.status_code == 201
    assert response.json()["username"] == "Jane Doe"


def test_create_users_invalid_json(test_app):
    response = test_app.post("/users/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "username"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.10/v/missing",
            }
        ]
    }

    response = test_app.post("/users/", data=json.dumps({"username": "a" * 51}))
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "String should have at most 50 characters"
    )


def test_read_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "John Doe"})
    )
    user_id = response.json()["id"]
    response = test_app_with_db.get(f"/users/{user_id}/")
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["username"] == "John Doe"
    # assert response_dict["created_at"]


def test_read_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/users/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "user not found"

    response = test_app_with_db.get("/users/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
                "url": "https://errors.pydantic.dev/2.10/v/greater_than",
            }
        ]
    }


def test_read_all_users(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "Joe Schmoe"})
    )
    user_id = response.json()["id"]
    response = test_app_with_db.get("/users/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == user_id, response_list))) == 1


def test_remove_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "John Smith"})
    )
    user_id = response.json()["id"]

    response = test_app_with_db.delete(f"/users/{user_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "username": "John Smith"}


def test_remove_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/users/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "user not found"

    response = test_app_with_db.delete("/users/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
                "url": "https://errors.pydantic.dev/2.10/v/greater_than",
            }
        ]
    }
