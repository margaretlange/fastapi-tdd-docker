from auth0.authentication import GetToken
from app.config import settings
from app.test.auth_data import token_directory


def get_test_token(token_name: str) -> str:
    if not getattr(settings, token_name):
        token = GetToken(
            settings.auth0_domain,
            settings.auth0_client_id,
            client_secret=settings.auth0_client_secret,
        )
        info_dict = token_directory[token_name].copy()
        token = token.login(**info_dict)
        token = token["access_token"]
        setattr(settings, token_name, token)
        return token
    return getattr(settings, token_name)
