
def test_status(test_app):
    response = test_app.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status_private(test_app, member_auth_header):
    response = test_app.get("/status/private", headers=member_auth_header)
    assert response.status_code == 200
    assert response.json() == {"status": "This is a private endpoint."}
