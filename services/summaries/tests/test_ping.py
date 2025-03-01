# project/tests/test_ping.py
from app.config import settings
from fastapi import APIRouter, Depends
from app import dependencies, authorization_header_elements
import pdb


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong", "testing": True}


def test_pongprivate(test_app):
    auth_headers = {
        "Authorization": f"Bearer {settings.jwt_test_token}",
        "Content-Type": "application/json"
    }
    response = test_app.get("/ping/private", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"ping": "This is a private endpoint"}


# not working
#def mock_get_bearer_token(header):
#        return "hello"
#    monkeypatch.setattr(authorization_header_elements, "get_bearer_token", mock_get_bearer_token)
#    pdb.set_trace()
#    def mock_validate_token(token):
#        return True
#    monkeypatch.setattr(dependencies, "validate_token", mock_validate_token)

