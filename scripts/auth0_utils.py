import argparse
import pdb
import jwt
from auth0.authentication import Database, GetToken
from auth0.management import Auth0
import time
import pathlib
import os
from dotenv import load_dotenv, set_key


def get_last_token_ts():
    top_folder = "%s/test_tokens" % (os.environ['HOME'])
    all_timestamps = os.listdir(top_folder)
    all_timestamps = [int(ts) for ts in all_timestamps]
    all_timestamps.sort()
    latest = all_timestamps[-1]
    return latest


def get_latest_token(admin=False):
    top_folder = "%s/test_tokens" % (os.environ['HOME'])
    latest = get_last_token_ts()
    if admin:
        filename = "admin_access_jwk.txt"
    else:
        filename = "member_access_jwk.txt"
    top_token_file = "%s/%s/%s" % (top_folder, latest, filename)
    with open(top_token_file, 'r') as fh:
        token = fh.read()
    return token


def make_token_folder(ts):
    folder = "%s/test_tokens/%s" % (os.environ['HOME'], ts)
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    return folder


def create_test_user(user_info, token, admin=False):
    database = Database(os.environ['AUTH0_DOMAIN'], os.environ['TEST_AUTH0_CLIENT_ID'])
    response = database.signup(**user_info)
    short_id = response["_id"]
    user_id = f"auth0|{short_id}"
    if admin:
        auth0 = Auth0(os.environ['AUTH0_DOMAIN'], token)
        roles = auth0.roles.list()
        role_id = roles['roles'][0]['id']
        auth0.roles.add_users(role_id, [user_id])


def validate_token(jwt_access_token, audience):
    auth0_issuer_url = f"https://{os.environ['AUTH0_DOMAIN']}/"
    # make sure to install cryptography library
    algorithm = "RS256"
    jwks_uri = f"{auth0_issuer_url}.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(jwks_uri)
    jwt_signing_key = jwks_client.get_signing_key_from_jwt(jwt_access_token).key
    payload = jwt.decode(
        jwt_access_token,
        jwt_signing_key,
        algorithms=algorithm,
        audience=audience,
        issuer=auth0_issuer_url,
    )
    return payload


def get_test_token_user(user_info):
    token = GetToken(
        os.environ['AUTH0_DOMAIN'], os.environ['TEST_AUTH0_CLIENT_ID'], client_secret=os.environ['TEST_AUTH0_CLIENT_SECRET']
    )
    token = token.login(**user_info)
    return token["access_token"]


def get_test_token():
    token = GetToken(
        os.environ['TEST_AUTH0_DOMAIN'], os.environ['TEST_AUTH0_CLIENT_ID'], client_secret=os.environ['TEST_AUTH0_CLIENT_SECRET']
    )
    token = token.client_credentials(os.environ['AUTH0_AUDIENCE'])
    token = token["access_token"]
    return token


def get_management_token():
    domain = os.environ['AUTH0_DOMAIN']
    token = GetToken(
        domain, os.environ['AUTH0_CLIENT_ID'], client_secret=os.environ['AUTH0_CLIENT_SECRET']
    )
    management_audience = f'https://{domain}/api/v2/'
    token = token.client_credentials(management_audience)
    token = token["access_token"]
    return token


def refresh_tokens(admin_info_token, member_info_token, ts):
    last_token_ts = get_last_token_ts()
    time_elapsed = ts - last_token_ts
    if time_elapsed > 86400:
        print("refreshing tokens")
        token_folder = make_token_folder(ts)
        admin_access_token = get_test_token_user(admin_info_token)
        validate_token(admin_access_token, os.environ['AUTH0_AUDIENCE'])
        with open(f'{token_folder}/admin_access_jwk.txt', 'w') as fh:
            fh.write(admin_access_token)

        member_access_token = get_test_token_user(member_info_token)
        validate_token(member_access_token, os.environ['AUTH0_AUDIENCE'])
        with open(f'{token_folder}/member_access_jwk.txt', 'w') as fh:
            fh.write(member_access_token)
    else:
        print("old tokens are still valid")


def write_tokens_to_config():
    home = os.environ['HOME']
    env_path = f"{home}/fastapi-tdd-docker/services/summaries/.env"
    # load_dotenv(dotenv_path=env_path)
    admin_token = get_latest_token(admin=True)
    member_token = get_latest_token(admin=False)
    set_key(env_path, "JWT_TEST_TOKEN_ADMIN", admin_token)
    set_key(env_path, "JWT_TEST_TOKEN_MEMBER", member_token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh_tokens", action="store_true",
                                help="Refresh test tokens for admin and member user")
    parser.add_argument("--create_users", action="store_true",
                                help="Create admin and member user")
    parser.add_argument("--update_config", action="store_true",
                                help="Update fastapi configuration file")
    parser.add_argument("--admin", action="store_true",
                                help="Print latest admin token")
    parser.add_argument("--member", action="store_true",
                                help="Print latest member token")
    args = parser.parse_args()
    refresh = args.refresh_tokens
    create_users = args.create_users
    update_config = args.update_config
    admin = args.admin
    member = args.member
    member_info = {
        "email": "testtwo@domain.com",
        "password": os.environ['AUTH0_TEST_MEMBER_PASSWORD'],
        "connection": "Username-Password-Authentication",
    }

    admin_info = {
        "email": "adminlady@domain.com",
        "password": os.environ['AUTH0_TEST_ADMIN_PASSWORD'],
        "connection": "Username-Password-Authentication",
    }

    admin_info_token = {
        "username": "adminlady@domain.com",
        "password": os.environ['AUTH0_TEST_ADMIN_PASSWORD'],
        "realm": "Username-Password-Authentication",
        "audience": os.environ['AUTH0_AUDIENCE']
    }
    member_info_token = {
        "username": "testtwo@domain.com",
        "password": os.environ['AUTH0_TEST_MEMBER_PASSWORD'],
        "realm": "Username-Password-Authentication",
        "audience": os.environ['AUTH0_AUDIENCE']
    }
    if refresh:
        now_ts = int(time.time())
        refresh_tokens(admin_info_token, member_info_token, now_ts)

    if create_users:
        token = get_management_token()
        domain = os.environ['AUTH0_DOMAIN']
        audience = f'https://{domain}/api/v2/'
        validate_token(token, audience)
        create_test_user(member_info, token, admin=False)
        create_test_user(admin_info, token, admin=True)

    ## you still must separately restart the docker container for the new environment to be recognized
    if update_config:
        now_ts = int(time.time())
        refresh_tokens(admin_info_token, member_info_token, now_ts)
        write_tokens_to_config()

    if admin:
        my_token = get_latest_token(admin=True)
        print(my_token)
    if member:
        my_token = get_latest_token(admin=False)
        print(my_token)

