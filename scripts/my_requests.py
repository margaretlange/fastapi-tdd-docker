import requests
import json
from contextlib import contextmanager


# url = "http://localhost:8000"
url = "https://mmldemo.com"


@contextmanager
def setup_test_user(member_auth_header):
    print("Adding current active user to database")
    response = requests.post(
            f"{url}/users/", data=json.dumps({"username": "Jane Doe"}), headers=member_auth_header
    )
    yield response
    print("Removing current active user from database")
    response = requests.delete(f"{url}/users/profile/", headers=member_auth_header)


def simple_test():
    # response = requests.get("http://localhost:8000/ping/private", headers=my_header)
    # print(response.json())
    response = requests.get(f"{url}/status/private", headers=my_header)
    return response.json()


def summary_test():
    response = requests.post(
                f"{url}/users/profile/summaries/",
                data=json.dumps({"query": "Who was Charles Darwin?"}),
                headers=my_header
        )
    return response.json()


if __name__ == "__main__":

    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZqTzR6NHFJM3lXWk02QmdCRk5CbyJ9.eyJpc3MiOiJodHRwczovL2Rldi1saG4xdWZxZ2tnejhsazV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2M3NjY0ZjY1N2QwZjRmN2FjOTA5YTYiLCJhdWQiOiJodHRwczovL2hlbGxvLXdvcmxkLmV4YW1wbGUuY29tIiwiaWF0IjoxNzQyMjM0OTE3LCJleHAiOjE3NDIzMjEzMTcsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidTg2a1ZQamo5WTVSeG9TWGd0SkR2QVhGT0tUZTVEUEciLCJwZXJtaXNzaW9ucyI6W119.U3GYhEdtX8vQpCHsjRrkFnZWURPR3-jI9Ccz7g7nzPB_-96l1IyDOrsaJeObMBfrCNAVDI1ahKLs58ibekJACDgpi8y279XYOf1mloZ7oV1q6UdojiQEWNv8Nb0HRroHCBcRoYLEqQoqo7zPiWU6Bzn7qtcNt7eWYSYmwuOkwTLXqr_nWqtbGHefwPFE-FrojpM7nYPPdYj6_ctn0FmNzjQKQSYC6GvYdXsdSSoSRlc5qF7ZnLww4lZSmo5LaP5NbyuGGNsS4KUTC3m45razAMvAnqLaI-tjj1NXA2BmcKqrD9v9zlB4AOQHuVkA8_pOcz095boQJjkX7WxNhHWd9g"

    my_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    with setup_test_user(my_header):
        print(simple_test())
