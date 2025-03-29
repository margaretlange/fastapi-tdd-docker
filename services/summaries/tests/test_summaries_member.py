# project/tests/test_summaries.py


import json

import pytest

from app.api import users

# import pdb


# make sure active user is in the database
@pytest.fixture(scope="module")
def setup_test_user(test_app_with_db, member_auth_header):
    print("Adding current active user to database")
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"username": "Jane Doe"}), headers=member_auth_header
    )
    yield response
    print("Removing current active user from database")
    response = test_app_with_db.delete("/users/profile/", headers=member_auth_header)


def test_create_summary(
    test_app_with_db, setup_test_user, monkeypatch, member_auth_header
):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)
    response = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin?"}),
        headers=member_auth_header,
    )

    assert response.status_code == 201
    assert response.json()["query"] == "Who was Charles Darwin?"


def test_create_summaries_invalid_json(test_app, member_auth_header):
    response = test_app.post(
        "/users/profile/summaries/", data=json.dumps({}), headers=member_auth_header
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "query"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
    response = test_app.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin"}),
        headers=member_auth_header,
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should match pattern '.*\\?$'"


def test_read_summary(
    test_app_with_db, setup_test_user, monkeypatch, member_auth_header
):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin?"}),
        headers=member_auth_header,
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.get(
        f"/users/profile/summaries/{summary_id}/", headers=member_auth_header
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["query"] == "Who was Charles Darwin?"
    assert response_dict["summary"] == ""
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(
    test_app_with_db, setup_test_user, member_auth_header
):
    response = test_app_with_db.get(
        "/users/profile/summaries/999/", headers=member_auth_header
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get(
        "/users/profile/summaries/0/", headers=member_auth_header
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
            }
        ]
    }


def test_read_all_summaries(
    test_app_with_db, setup_test_user, monkeypatch, member_auth_header
):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin?"}),
        headers=member_auth_header,
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.get(
        "/users/profile/summaries/", headers=member_auth_header
    )
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(
    test_app_with_db, setup_test_user, monkeypatch, member_auth_header
):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)
    response = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Abraham Lincoln?"}),
        headers=member_auth_header,
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(
        f"/users/profile/summaries/{summary_id}/", headers=member_auth_header
    )
    assert response.status_code == 200
    assert response.json()["id"] == summary_id
    assert response.json()["query"] == "Who was Abraham Lincoln?"


def test_remove_summary_incorrect_id(
    test_app_with_db, setup_test_user, member_auth_header
):
    response = test_app_with_db.delete(
        "/users/profile/summaries/999/", headers=member_auth_header
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.delete(
        "/users/profile/summaries/0/", headers=member_auth_header
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
            }
        ]
    }


def test_update_summary(test_app_with_db, monkeypatch, member_auth_header):
    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)

    response = test_app_with_db.post(
        "/users/profile/summaries/",
        data=json.dumps({"query": "Who was Charles Darwin?"}),
        headers=member_auth_header,
    )
    summary_id = response.json()["id"]
    response = test_app_with_db.put(
        f"/users/profile/summaries/{summary_id}/",
        data=json.dumps({"query": "Who was Charles Darwin?", "summary": "updated!"}),
        headers=member_auth_header,
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["query"] == "Who was Charles Darwin?"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"query": "Who was Charles Darwin?", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"query": "Who was Charles Darwin?", "summary": "updated!"},
            422,
            [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "query"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                },
            ],
        ],
        [
            1,
            {"query": "Who was Charles Darwin?"},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {"query": "Who was Charles Darwin?"},
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app_with_db, member_auth_header, summary_id, payload, status_code, detail
):
    response = test_app_with_db.put(
        f"/users/profile/summaries/{summary_id}/",
        data=json.dumps(payload),
        headers=member_auth_header,
    )
    assert response.status_code == status_code
    print(response.json()["detail"])
    assert response.json()["detail"] == detail
