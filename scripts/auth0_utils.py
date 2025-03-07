import argparse
import pdb
import jwt
from auth0.authentication import Database, GetToken
from auth0.management.users import Users


# example sub for admin 'auth0|67c91c0d56e672bbc7bf0e4b'


def create_test_user(args, user_info, admin=False):
    database = Database(args.AUTH0_DOMAIN, args.AUTH0_CLIENT_ID)
    response = database.signup(**user_info)
    # had to do this through dashboard
    U = Users(args.AUTH0_DOMAIN, args.MANAGEMENT_API_KEY)
    if admin:
        U.add_roles(response["_id"], ["admin"])


# removing errors since my goal is just inspection
def validate_token(args, jwt_access_token):
    auth0_issuer_url = f"https://{args.AUTH0_DOMAIN}/"
    # make sure to install cryptography library
    algorithm = "RS256"
    jwks_uri = f"{auth0_issuer_url}.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(jwks_uri)
    jwt_signing_key = jwks_client.get_signing_key_from_jwt(jwt_access_token).key
    payload = jwt.decode(
        jwt_access_token,
        jwt_signing_key,
        algorithms=algorithm,
        audience=args.AUTH0_AUDIENCE,
        issuer=auth0_issuer_url,
    )
    pdb.set_trace()
    return payload


def get_test_token_user(args, user_info):
    token = GetToken(
        args.AUTH0_DOMAIN, args.AUTH0_CLIENT_ID, client_secret=args.AUTH0_CLIENT_SECRET
    )
    token = token.login(**user_info)
    return token["access_token"]


def get_test_token(args):
    token = GetToken(
        args.AUTH0_DOMAIN, args.AUTH0_CLIENT_ID, client_secret=args.AUTH0_CLIENT_SECRET
    )
    token = token.client_credentials(args.AUTH0_AUDIENCE)
    token = token["access_token"]
    return token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Auth0 script to create user and get tokens"
    )
    parser.add_argument("--AUTH0_DOMAIN", required=True, help="Auth0 domain")
    parser.add_argument("--AUTH0_CLIENT_ID", required=True, help="Auth0 client ID")
    parser.add_argument(
        "--AUTH0_CLIENT_SECRET", required=True, help="Auth0 client secret"
    )
    parser.add_argument("--AUTH0_AUDIENCE", required=True, help="Auth0 audience")
    parser.add_argument("--MEMBER_PASSWORD", required=True, help="Test member password")
    parser.add_argument("--ADMIN_PASSWORD", required=True, help="Test admin password")

    args = parser.parse_args()
    member_info = {
        "email": "testtwo@domain.com",
        "password": args.MEMBER_PASSWORD,
        "connection": "Username-Password-Authentication",
    }

    admin_info = {
        "email": "adminlady@domain.com",
        "password": args.ADMIN_PASSWORD,
        "connection": "Username-Password-Authentication",
    }

    admin_info_token = {
        "username": "adminlady@domain.com",
        "password": args.ADMIN_PASSWORD,
        "realm": "Username-Password-Authentication",
        "audience": args.AUTH0_AUDIENCE,
    }
    member_info_token = {
        "username": "testtwo@domain.com",
        "password": args.MEMBER_PASSWORD,
        "realm": "Username-Password-Authentication",
        "audience": args.AUTH0_AUDIENCE,
    }

    access_token = get_test_token_user(args, admin_info_token)
    print(access_token)
    validate_token(args, access_token)
    # Example usage
    # create_test_user(args, admin_info, admin=True)
    #     # token = get_test_token(args)
