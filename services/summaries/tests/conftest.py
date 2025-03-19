# project/tests/conftest.py


import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application  # updated
from app.test.auth_utils import get_test_token


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    app = create_application()  # new
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:  # updated
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def member_auth_header():
    token = get_test_token('jwt_test_token_member')
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header


@pytest.fixture(scope="session")
def admin_auth_header():
    token = get_test_token('jwt_test_token_admin')
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header
