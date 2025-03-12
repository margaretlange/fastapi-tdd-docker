import requests
import json
from contextlib import contextmanager


@contextmanager
def setup_test_user(member_auth_header):
    print("Adding current active user to database")
    response = requests.post(
            "http://localhost:8000/users/", data=json.dumps({"username": "Jane Doe"}), headers=member_auth_header
    )
    yield response
    print("Removing current active user from database")
    response = requests.delete("http://localhost:8000/users/profile/", headers=member_auth_header)


def simple_test():
    # response = requests.get("http://localhost:8000/ping/private", headers=my_header)
    # print(response.json())
    response = requests.get("http://localhost:8000/ping/private", headers=my_header)
    return response.json()


if __name__ == "__main__":
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZqTzR6NHFJM3lXWk02QmdCRk5CbyJ9.eyJpc3MiOiJodHRwczovL2Rldi1saG4xdWZxZ2tnejhsazV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2M3NjY0ZjY1N2QwZjRmN2FjOTA5YTYiLCJhdWQiOiJodHRwczovL2hlbGxvLXdvcmxkLmV4YW1wbGUuY29tIiwiaWF0IjoxNzQxNzI5NTM4LCJleHAiOjE3NDE4MTU5MzgsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidTg2a1ZQamo5WTVSeG9TWGd0SkR2QVhGT0tUZTVEUEciLCJwZXJtaXNzaW9ucyI6W119.oSsHaMRSDh5CnQwiJIipBiRCbXD-oBZaMwOZTq9FtNEln5azC_RmoNu2XY_GFSwGefo-29GYc7cCbqgEpQP0mP1Cp2EDLK7IJBIZkB6o3xbq7x5cmVIeEL_0Vp5iR55B2KUU3V-LaDGyXH6JuLko9ASgG_pGpUacesjoQGRS0Gl5PGlecgpM2_803Vv1A87hHAxTwpLlNk0xB51NUMFbTPL4ScLV4ooWK9K4S2emqd_J8PPnLZ43O_GDSTkyPjfsdwOANHqjSk-wAv9hvl7STC8EQ1bt0vufwXrQcXBaNkYmAzLajYAt3QQsRvDsT1j_mebaKd5I6WZBbxe_OeiTgg"

    my_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    with setup_test_user(my_header):
        response = requests.post(
                "http://localhost:8000/users/profile/summaries/",
                data=json.dumps({"query": "Who was Charles Darwin?"}),
                headers=my_header
        )
        print(response)
