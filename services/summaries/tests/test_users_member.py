# project/tests/test_users.py

import json

# import pdb
# right now set up and clean up are in the tests so they have to run in order


def test_create_users_invalid_json(test_app, member_auth_header):
    response = test_app.post("/users/", data=json.dumps({}), headers=member_auth_header)

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
    response = test_app.post(
        "/users/", headers=member_auth_header, data=json.dumps({"username": "a" * 51})
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "String should have at most 50 characters"
    )


def test_create_user(test_app_with_db, member_auth_header):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "Jane Doe"}), headers=member_auth_header
    )
    assert response.status_code == 201
    assert response.json()["username"] == "Jane Doe"


def test_read_current_active_user(test_app_with_db, member_auth_header):
    response = test_app_with_db.get("/users/profile/", headers=member_auth_header)
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"]
    assert response_dict["username"] == "Jane Doe"
    assert response_dict["created_at"]
    assert response_dict["auth_sub"]


def test_remove_current_active_user(test_app_with_db, member_auth_header):
    response = test_app_with_db.delete("/users/profile/", headers=member_auth_header)
    assert response.status_code == 200
    assert response.json()["username"] == "Jane Doe"
