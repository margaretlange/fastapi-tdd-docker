# project/tests/conftest.py


import os

import pytest
from auth0.authentication import GetToken
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings, settings
from app.main import create_application  # updated

import pdb


def get_set_token_admin():
    admin_info = {
        "username": "adminlady@domain.com",
        "password": settings.test_admin_password,
        "realm": "Username-Password-Authentication",
        "audience": settings.auth0_audience,
    }
    if not settings.jwt_test_token_admin:
        token = GetToken(
            settings.auth0_domain,
            settings.auth0_client_id,
            client_secret=settings.auth0_client_secret,
        )
        token = token.login(**admin_info)
        token = token["access_token"]
        settings.jwt_test_token_admin = token
        return token
    return settings.jwt_test_token_admin


def get_set_token_member():
    member_info = {
        "username": "testtwo@domain.com",
        "password": settings.test_member_password,
        "realm": "Username-Password-Authentication",
        "audience": settings.auth0_audience,
    }
    if not settings.jwt_test_token_member:
        token = GetToken(
            settings.auth0_domain,
            settings.auth0_client_id,
            client_secret=settings.auth0_client_secret,
        )
        token = token.login(**member_info)
        token = token["access_token"]
        settings.jwt_test_token_member = token
        return token
    return settings.jwt_test_token_member


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
    token = get_set_token_member()
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header


@pytest.fixture(scope="session")
def admin_auth_header():
    token = get_set_token_admin()
    auth_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return auth_header


# @pytest.fixture
# def mock_validate_token(monkeypatch):
#    def mock_inner(*args, **kwargs):
#        return True
#    monkeypatch.setattr(dependencies, "validate_token", mock_inner)
