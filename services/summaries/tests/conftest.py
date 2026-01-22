# project/tests/conftest.py


import os

# import pdb
import pytest
import logging
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.dependencies import mock_validate_token, validate_token
from app.main import create_application  # updated
from tests.auth_utils import (
    get_test_token_member,
    mock_get_test_token_admin,
    mock_get_test_token_member,
)

from tests.auth_utils import get_test_token_admin  # isort:skip

logger = logging.getLogger("uvicorn")


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        help="run tests against auth0 authentication",
    )


@pytest.fixture(scope="session")
def integration(request):
    return request.config.getoption("--integration")


@pytest.fixture(scope="session")
def member_auth_header(integration):
    if integration:
        token = get_test_token_member()
    else:
        token = mock_get_test_token_member()
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header


@pytest.fixture(scope="session")
def admin_auth_header(integration):
    if integration:
        token = get_test_token_admin()
    else:
        token = mock_get_test_token_admin()
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header


@pytest.fixture(scope="module")
def test_app(integration):
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    if not integration:
        app.dependency_overrides[validate_token] = mock_validate_token
    with TestClient(app) as test_client:  # updated
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db(integration):
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    if not integration:
        app.dependency_overrides[validate_token] = mock_validate_token
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
