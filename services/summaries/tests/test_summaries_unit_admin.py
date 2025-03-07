# project/tests/test_summaries_unit.py


import datetime


from app.api import crud
from app.models.tortoise import SummarySchema
import pdb


def test_read_summary(test_app, monkeypatch, admin_auth_header):
    user_info = {"username": "Jane Doe", "id": 1, "created_at": "2024-12-31T23:59:59Z", "auth_sub": "usersub"}

    test_data = {
        "id": 1,
        "user": user_info,
        "query": "Who was Charles Darwin?",
        "summary": "summary",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_get(id, user_id):
        return test_data

    monkeypatch.setattr(crud, "get_summary", mock_get)
    response = test_app.get("/users/1/summaries/1/", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch, admin_auth_header):
    async def mock_get(id, user_id):
        return None

    monkeypatch.setattr(crud, "get_summary", mock_get)

    response = test_app.get("/users/1/summaries/999/", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch, admin_auth_header):
    user_info = {"username": "Jane Doe", "id": 1, "created_at": "2024-12-31T23:59:59Z", "auth_sub": "usersub"}
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

    monkeypatch.setattr(crud, "get_all_summaries", mock_get_all)

    response = test_app.get("/users/1/summaries/", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch, admin_auth_header):
    user_info = {"username": "Jane Doe", "id": 1, "created_at": "2024-12-31T23:59:59Z", "auth_sub": "usersub"}
    test_data = {
        "id": 1,
        "user": user_info,
        "query": "Who was Charles Darwin?",
        "summary": "A guy",
        "created_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    async def mock_get(id, user_id):
        return SummarySchema(**test_data)

    monkeypatch.setattr(crud, "get_summary", mock_get)

    async def mock_delete(id, user_id):
        return 1, 1

    monkeypatch.setattr(crud, "delete_summary", mock_delete)
    response = test_app.delete("/users/1/summaries/1/", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json() == {
        "query": "Who was Charles Darwin?",
        "id": 1,
        "user_id": 1,
    }


def test_remove_summary_incorrect_id(test_app, monkeypatch, admin_auth_header):
    async def mock_get(id, user_id):
        return None

    monkeypatch.setattr(crud, "get_summary", mock_get)

    response = test_app.delete("/users/1/summaries/999/", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"
