
def test_status_admin(test_app, admin_auth_header):
    response = test_app.get("/status/admin/", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json() == {"status": "This is an admin endpoint."}
