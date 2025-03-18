import requests
import json
from contextlib import contextmanager

import pdb
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


def simple_test(my_header):
    response = requests.get(f"{url}/status/private/", headers=my_header)
    return response.json()


def summary_test(my_header):
    response = requests.post(
                f"{url}/users/profile/summaries/",
                data=json.dumps({"query": "Who was Charles Darwin?"}),
                headers=my_header
        )
    return response.json()


if __name__ == "__main__":
# add arg parse for tokens
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZqTzR6NHFJM3lXWk02QmdCRk5CbyJ9.eyJpc3MiOiJodHRwczovL2Rldi1saG4xdWZxZ2tnejhsazV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2M5MWMwZDU2ZTY3MmJiYzdiZjBlNGIiLCJhdWQiOiJodHRwczovL2hlbGxvLXdvcmxkLmV4YW1wbGUuY29tIiwiaWF0IjoxNzQyMjQzNDEwLCJleHAiOjE3NDIzMjk4MTAsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidTg2a1ZQamo5WTVSeG9TWGd0SkR2QVhGT0tUZTVEUEciLCJwZXJtaXNzaW9ucyI6WyJyZWFkOnN1bW1hcmllcy1pbmZvIiwicmVhZDp1c2Vycy1pbmZvIl19.TpKI0INYGKJcImheTYVkHxfJ16IT1x0czWwuV5a1oclFfY1DaFlMmYkVZx9GVlWXdRb5Bvlb4bYnEEP2UraHpN2IksFJc1fz2clDn4bsf5X1qOwH7rYvKvk8wzuYBUQCDH8Y5lmYI8yxuHXGnQdPzugM3-UbyJL7vKLJyn32I30Z31u8syrAtmi1ALUdgV6Z5TFpBjwG0FCWSSAszf2nGzY4lf09hXa2YKG5UMeByKI0TdUcsvLKiuBacsPz9TewDMJ5ZXo8157js5QaTpzzEuuZnAUqQhzsqca-qWLb3IZpDGIUW7pX_5VSf7AnUM_M9LLuk0RwYSp6uPvyezVx9A"
    my_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    with setup_test_user(my_header):
        print(summary_test(my_header))
