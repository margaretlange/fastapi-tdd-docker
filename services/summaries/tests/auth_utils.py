import datetime
from functools import partial

import jwt
from auth0.authentication import GetToken

from app.config import settings
from tests.auth_data import token_directory


def get_test_token(token_name: str) -> str:
    if not getattr(settings, token_name):
        token = GetToken(
            settings.auth0_domain,
            settings.auth0_client_id,
            client_secret=settings.auth0_client_secret,
        )
        info_dict = token_directory[token_name].copy()
        # drop unneeded keys from dictionary now
        # make do classes and subclasses later
        del info_dict["sub"]
        del info_dict["permissions"]
        token = token.login(**info_dict)
        token = token["access_token"]
        setattr(settings, token_name, token)
        return token
    return getattr(settings, token_name)


get_test_token_member = partial(get_test_token, "jwt_test_token_member")
get_test_token_admin = partial(get_test_token, "jwt_test_token_admin")


def mock_get_test_token(token_name: str) -> str:
    info_dict = token_directory[token_name].copy()
    payload = {
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(seconds=86400),  # updated
        "iat": datetime.datetime.now(datetime.UTC),
        "sub": info_dict["sub"],
        "permissions": info_dict["permissions"],
    }
    return jwt.encode(payload, settings.jwt_test_encode_key, algorithm="HS256")


mock_get_test_token_member = partial(mock_get_test_token, "jwt_test_token_member")
mock_get_test_token_admin = partial(mock_get_test_token, "jwt_test_token_admin")


def mock_validate(token: str) -> dict:
    payload = jwt.decode(token, settings.jwt_test_encode_key, algorithms="HS256")
    return payload
