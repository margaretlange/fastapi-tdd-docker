# project/tests/test_summaries_unit.py


import datetime
import json

import pytest

from app.api import crud, summaries


def test_create_summary(test_app, monkeypatch):
    test_request_payload = {"query": "Who was Charles Darwin?"}
    test_response_payload = {"id": 1, "query": "Who was Charles Darwin?"}

    async def mock_post(payload):
        return 1

    def mock_generate_summary(summary_id, query):
        return None

    monkeypatch.setattr(crud, "post_summary", mock_post)
    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)
    response = test_app.post(
        "/summaries/",
        data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "query"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.10/v/missing",
            }
        ]
    }

    response = test_app.post(
        "/summaries/", data=json.dumps({"query": "Who was Charles Darwin"})
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should match pattern '.*\\?$'"


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "query": "Who was Charles Darwin?",
        "summary": "summary",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get_summary", mock_get)

    response = test_app.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_summary", mock_get)

    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "query": "Who was Charles Darwin?",
            "summary": "summary",
            "created_at": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
        {
            "id": 2,
            "query": "Who was Ada Lovelace?",
            "summary": "summary",
            "created_at": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all_summaries", mock_get_all)

    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "query": "Who was Charles Darwin?",
            "summary": "summary",
            "created_at": datetime.datetime.now(datetime.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
        }

    monkeypatch.setattr(crud, "get_summary", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete_summary", mock_delete)

    response = test_app.delete("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "query": "Who was Charles Darwin?"}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_summary", mock_get)

    response = test_app.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {"query": "Who was Charles Darwin?", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "query": "Who was Charles Darwin?",
        "summary": "summary",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put_summary", mock_put)

    response = test_app.put(
        "/summaries/1/",
        data=json.dumps(test_request_payload),
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
                    "url": "https://errors.pydantic.dev/2.10/v/greater_than",
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
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
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
                    "url": "https://errors.pydantic.dev/2.10/v/missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app, monkeypatch, summary_id, payload, status_code, detail
):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put_summary", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_query(test_app):
    response = test_app.put(
        "/summaries/1/",
        data=json.dumps({"query": "Who was Charles Darwin", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should match pattern '.*\\?$'"
