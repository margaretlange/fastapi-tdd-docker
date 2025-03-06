import json

# import pdb


# do set up and tear down though later
class TestUserAdmin:
    user_id: int = 0

    def test_create_user(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.post(
            "/users/",
            data=json.dumps({"username": "Jane Doe"}),
            headers=admin_auth_header,
        )
        assert response.status_code == 201
        assert response.json()["username"] == "Jane Doe"
        assert response.json()["id"]
        TestUserAdmin.user_id = response.json()["id"]

    def test_read_user(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.get(
            f"/users/{TestUserAdmin.user_id}/", headers=admin_auth_header
        )
        assert response.status_code == 200
        response_dict = response.json()
        assert response_dict["id"] == self.user_id
        assert response_dict["username"] == "Jane Doe"
        assert response_dict["created_at"]
        assert response_dict["auth_sub"]

    def test_read_user_incorrect_id(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.get("/users/999/", headers=admin_auth_header)
        assert response.status_code == 404
        assert response.json()["detail"] == "user not found"

        response = test_app_with_db.get("/users/0/", headers=admin_auth_header)
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "ctx": {"gt": 0},
                    "input": "0",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "type": "greater_than",
                    "url": "https://errors.pydantic.dev/2.10/v/greater_than",
                }
            ]
        }

    def test_read_all_users(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.get("/users/", headers=admin_auth_header)
        assert response.status_code == 200

        response_list = response.json()
        assert len(list(filter(lambda d: d["id"] == self.user_id, response_list))) == 1

    def test_remove_user_incorrect_id(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.delete("/users/999/", headers=admin_auth_header)
        assert response.status_code == 404
        assert response.json()["detail"] == "user not found"

        response = test_app_with_db.delete("/users/0/", headers=admin_auth_header)
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "ctx": {"gt": 0},
                    "input": "0",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "type": "greater_than",
                    "url": "https://errors.pydantic.dev/2.10/v/greater_than",
                }
            ]
        }

    def test_remove_user(self, test_app_with_db, admin_auth_header):
        response = test_app_with_db.delete(
            f"/users/{TestUserAdmin.user_id}/", headers=admin_auth_header
        )
        assert response.status_code == 200
        assert response.json() == {"id": TestUserAdmin.user_id, "username": "Jane Doe"}
