# project/tests/test_summaries.py


import json

import pytest

from app.api import users

# import pdb


# make sure a member ("John Smith") is in the database
# this should be module level but monkeypatch is function level so working on it
@pytest.fixture(scope="function")
def setup_user_info(test_app_with_db, monkeypatch, member_auth_header):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)

    print("Adding current active user and summary to database")
    response_one = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "John Smith"}), headers=member_auth_header
    )
    response_two = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin?"}),
        headers=member_auth_header,
    )
    summary_id = response_two.json()["id"]
    yield (response_one.json()["id"], summary_id)
    print("Removing current active user and summary from database")
    test_app_with_db.delete("/users/profile/", headers=member_auth_header)
    test_app_with_db.delete(
        f"/users/profile/summaries/{summary_id}", headers=member_auth_header
    )


def test_read_summary(test_app_with_db, setup_user_info, admin_auth_header):
    user_id, summary_id = setup_user_info

    response = test_app_with_db.get(
        f"/users/{user_id}/summaries/{summary_id}/", headers=admin_auth_header
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["query"] == "Who was Charles Darwin?"
    assert response_dict["summary"] == ""
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(
    test_app_with_db, setup_user_info, admin_auth_header
):
    user_id, summary_id = setup_user_info
    response = test_app_with_db.get(
        f"/users/{user_id}/summaries/999/", headers=admin_auth_header
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get(
        f"/users/{user_id}/summaries/0/", headers=admin_auth_header
    )
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


def test_read_all_summaries(test_app_with_db, setup_user_info, admin_auth_header):
    user_id, summary_id = setup_user_info

    response = test_app_with_db.get(
        f"/users/{user_id}/summaries/", headers=admin_auth_header
    )
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db, setup_user_info, admin_auth_header):
    user_id, summary_id = setup_user_info

    response = test_app_with_db.delete(
        f"/users/{user_id}/summaries/{summary_id}/", headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": summary_id,
        "user_id": user_id,
        "query": "Who was Charles Darwin?",
    }


def test_remove_summary_incorrect_id(
    test_app_with_db, setup_user_info, admin_auth_header
):
    user_id, summary_id = setup_user_info
    response = test_app_with_db.delete(
        f"/users/{user_id}/summaries/999/", headers=admin_auth_header
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.delete(
        f"/users/{user_id}/summaries/0/", headers=admin_auth_header
    )
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
