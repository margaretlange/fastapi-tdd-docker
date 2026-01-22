import requests
import json
from contextlib import contextmanager
from auth0_utils import get_latest_token


import pdb
url = "http://localhost:8000"
# url = "https://mmldemo.com"


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
    token = get_latest_token(admin=True)
    my_header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    res = simple_test(my_header)
    pdb.set_trace()
    # with setup_test_user(my_header):
    #    print(summary_test(my_header))
