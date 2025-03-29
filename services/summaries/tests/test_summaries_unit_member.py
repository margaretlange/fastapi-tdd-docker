# project/tests/test_summaries_unit.py


import datetime
import json

import pytest

from app.api import crud, users
from app.models.tortoise import SummarySchema


def test_create_summary(test_app, monkeypatch, member_auth_header):
    test_request_payload = {"query": "Who was Charles Darwin?"}
    test_response_payload = {"id": 1, "user_id": 1, "query": "Who was Charles Darwin?"}

    async def mock_post(user_id, payload):
        return 1, 1

    def mock_generate_summary(summary_id, user_id, query):
        return None

    monkeypatch.setattr(crud, "post_current_active_user_summary", mock_post)
    monkeypatch.setattr(users, "generate_summary", mock_generate_summary)
    response = test_app.post(
        "/users/profile/summaries/",
        data=json.dumps(test_request_payload),
        headers=member_auth_header,
    )
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app, member_auth_header):
    response = test_app.post(
        "/users/profile/summaries/", data=json.dumps({}), headers=member_auth_header
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "query"],
                "msg": "Field required",
                "input": {},
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


def test_read_summary(test_app, monkeypatch, member_auth_header):
    user_info = {
        "username": "Jane Doe",
        "id": 1,
        "created_at": "2024-12-31T23:59:59Z",
        "auth_sub": "mysub",
    }

    test_data = {
        "id": 1,
        "user": user_info,
        "query": "Who was Charles Darwin?",
        "summary": "summary",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_get(id, auth_sub):
        return test_data

    monkeypatch.setattr(crud, "get_current_active_user_summary", mock_get)
    response = test_app.get("/users/profile/summaries/1/", headers=member_auth_header)
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch, member_auth_header):
    async def mock_get(id, auth_sub):
        return None

    monkeypatch.setattr(crud, "get_current_active_user_summary", mock_get)

    response = test_app.get("/users/profile/summaries/999/", headers=member_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch, member_auth_header):
    user_info = {
        "username": "Jane Doe",
        "id": 1,
        "created_at": "2024-12-31T23:59:59Z",
        "auth_sub": "mysub",
    }
    test_data = [
        {
            "user": user_info,
            "id": 1,
            "query": "Who was Charles Darwin?",
            "summary": "summary",
            "created_at": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
        {
            "user": user_info,
            "id": 2,
            "query": "Who was Ada Lovelace?",
            "summary": "summary",
            "created_at": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
    ]

    async def mock_get_all(user_id):
        return test_data

    monkeypatch.setattr(crud, "get_current_active_user_summaries", mock_get_all)

    response = test_app.get("/users/profile/summaries/", headers=member_auth_header)
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch, member_auth_header):
    user_info = {
        "username": "Jane Doe",
        "id": 1,
        "created_at": "2024-12-31T23:59:59Z",
        "auth_sub": "mysub",
    }
    test_data = {
        "id": 1,
        "user": user_info,
        "query": "Who was Charles Darwin?",
        "summary": "A guy",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_get(id, auth_sub):
        return SummarySchema(**test_data)

    monkeypatch.setattr(crud, "get_current_active_user_summary", mock_get)

    async def mock_delete(id, auth_sub):
        return 1, 1

    monkeypatch.setattr(crud, "delete_current_active_user_summary", mock_delete)
    response = test_app.delete(
        "/users/profile/summaries/1/", headers=member_auth_header
    )
    assert response.status_code == 200
    assert response.json() == {
        "query": "Who was Charles Darwin?",
        "id": 1,
        "user_id": 1,
    }


def test_remove_summary_incorrect_id(test_app, monkeypatch, member_auth_header):
    async def mock_get(id, user_id):
        return None

    monkeypatch.setattr(crud, "get_current_active_user_summary", mock_get)

    response = test_app.delete(
        "/users/profile/summaries/999/", headers=member_auth_header
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch, member_auth_header):
    user_info = {
        "username": "Jane Doe",
        "id": 1,
        "created_at": "2024-12-31T23:59:59Z",
        "auth_sub": "auth_sub",
    }
    test_request_payload = {"query": "Who was Charles Darwin?", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "user": user_info,
        "query": "Who was Charles Darwin?",
        "summary": "summary",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_put(id, auth_sub, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put_current_active_user_summary", mock_put)

    response = test_app.put(
        "/users/profile/summaries/1/",
        data=json.dumps(test_request_payload),
        headers=member_auth_header,
    )
    assert response.status_code == 200
    assert response.json() == test_response_payload


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
        [
            1,
            {"query": "Who was Charles Darwin", "summary": "old summary"},
            422,
            [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "query"],
                    "msg": "String should match pattern '.*\\?$'",
                    "ctx": {"pattern": ".*\\?$"},
                    "input": "Who was Charles Darwin",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app,
    monkeypatch,
    member_auth_header,
    summary_id,
    payload,
    status_code,
    detail,
):
    async def mock_put(user_id, id, payload):
        return None

    monkeypatch.setattr(crud, "put_current_active_user_summary", mock_put)

    response = test_app.put(
        f"/users/profile/summaries/{summary_id}/",
        data=json.dumps(payload),
        headers=member_auth_header,
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail
