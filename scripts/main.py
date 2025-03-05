 
import argparse
import pdb
import jwt
import time


# JWT_ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZqTzR6NHFJM3lXWk02QmdCRk5CbyJ9.eyJpc3MiOiJodHRwczovL2Rldi1saG4xdWZxZ2tnejhsazV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ1ODZrVlBqajlZNVJ4b1NYZ3RKRHZBWEZPS1RlNURQR0BjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9oZWxsby13b3JsZC5leGFtcGxlLmNvbSIsImlhdCI6MTc0MTEyMTE3NiwiZXhwIjoxNzQxMjA3NTc2LCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJ1ODZrVlBqajlZNVJ4b1NYZ3RKRHZBWEZPS1RlNURQRyJ9.bUz_3qXtzlDbs5YYS9sXxsCduGuklDUIFxpdP2x7OlLbAwWHZAyqS1GJUJIVc_gJ7UvbXMcDxmpMgTrFLsVN_DaMjWk2sIa4KO0C7v2LtUMD4ojf2gi2tbS_e4k6s8yDaNEPvgNk4OEiShKN6eUUXUNm_Zid6CZDwNIurnmOTi80wTtrwIt9aKdUmqWj1y6x-cnKAwuVq53rFWwdbKnYNKQ4BIyaY95OLPjcth-T1x1rC9OWSj9NuZ_IAiUD96vCuAJSzl0PijjIpb8VlTPy6EODj7l2xXFO8z7TF6sd6vi_Avph9LoEEwU_zdKC9DEI0R6tcwLP3I5o6Qnhjyvk0g'
# 'u86kVPjj9Y5RxoSXgtJDvAXFOKTe5DPG@clients'

# JWT_ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZqTzR6NHFJM3lXWk02QmdCRk5CbyJ9.eyJpc3MiOiJodHRwczovL2Rldi1saG4xdWZxZ2tnejhsazV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ1ODZrVlBqajlZNVJ4b1NYZ3RKRHZBWEZPS1RlNURQR0BjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9oZWxsby13b3JsZC5leGFtcGxlLmNvbSIsImlhdCI6MTc0MTIwNTgwNiwiZXhwIjoxNzQxMjkyMjA2LCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJ1ODZrVlBqajlZNVJ4b1NYZ3RKRHZBWEZPS1RlNURQRyJ9.jnCW7pb5xhIEhavaSzoAf8Varzvu6fcbRz-tzhGPtRGyManxi9fP_EH4TlB830JFH9jKeh1ZRH0l0x31yGQxgEyCyI7vdpwh8fgXWs2QPB1Bc5avfLJE1_A1WW8kVPBEI-W26V1wA71yxnRflT_KI5LzZPwViRKWi4vjishsAqIgl_IGLi8YuKZdp7ZNwumM-ytQOjYk_7Xtr1woKz5k7ANkU7oP-m_k983IfuTmjH4hpLVbBuHabQSAxIxf_Zwis_5Kp7_Gg4CdCq9VtdM_OslFGt8O6-s30AXPgvHpUfm9UlAhSh9y92hw_7OyldiYgMcD4ppQ3_oTKB5r0EGT5A' 
# sub 'u86kVPjj9Y5RxoSXgtJDvAXFOKTe5DPG@clients'
# does sub field stay the same?

def create_test_user(args):
    database = Database(args.AUTH0_DOMAIN, args.AUTH0_CLIENT_ID)
    database.signup(
        email="testtwo@domain.com",
        password="zhD>73YSgN_",
        connection="Username-Password-Authentication",
    )


# removing errors since my goal is just inspection
def validate_token(args):
    auth0_issuer_url = f"https://{args.AUTH0_DOMAIN}/"
    # make sure to install cryptography library
    algorithm = "RS256"
    jwks_uri = f"{auth0_issuer_url}.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(jwks_uri)
    jwt_signing_key = jwks_client.get_signing_key_from_jwt(
        JWT_ACCESS_TOKEN
    ).key
    payload = jwt.decode(
                JWT_ACCESS_TOKEN,
                jwt_signing_key,
                algorithms=algorithm,
                audience=args.AUTH0_AUDIENCE,
                issuer=auth0_issuer_url,
            )
    pdb.set_trace()
    return payload

# this is not always working
# sometimes works second try
def get_test_token_user(args):
    token = GetToken(
        args.AUTH0_DOMAIN, args.AUTH0_CLIENT_ID, client_secret=args.AUTH0_CLIENT_SECRET
    )
    token.login(
        username="testtwo@domain.com",
        password="zhD>73YSgN_",
        realm="Username-Password-Authentication",
    )
    # is this necessary
    print("sleeping")
    time.sleep(10)
    token.client_credentials(args.AUTH0_AUDIENCE)
    pdb.set_trace()
    token = token["access_token"]
    return token


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

    args = parser.parse_args()
    validate_token(args)
    # Example usage
    # create_test_user(args)
    # token = get_test_token_user(args)
    # token = get_test_token(args)
    #print(token)
    # token = get_test_token(args)
    # print(f"Client token: {token}")
