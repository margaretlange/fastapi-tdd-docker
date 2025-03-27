# project/app/config.py

import logging
from functools import lru_cache

from pydantic import AnyUrl, validator
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = 0
    database_url: AnyUrl = None
    jwt_test_encode_key: str

    client_origin_url: str | None = None

    # for simple testing setup on github actions these aren't needed
    auth0_audience: str | None = None
    auth0_domain: str | None = None
    auth0_client_id: str | None = None
    auth0_client_secret: str | None = None

    test_member_password: str | None = None
    test_admin_password: str | None = None

    jwt_test_token_member: str | None = None
    jwt_test_token_admin: str | None = None

    @classmethod
    @validator("client_origin_url", "auth0_audience", "auth0_domain")
    def check_not_empty(cls, v):
        assert v != "", f"{v} is not defined"
        return v


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()
