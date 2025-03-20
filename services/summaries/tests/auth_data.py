from app.config import settings

admin_info = {
    "username": "adminlady@domain.com",
    "password": settings.test_admin_password,
    "realm": "Username-Password-Authentication",
    "audience": settings.auth0_audience,
    "sub": "auth0|67c91c0d56e672bbc7bf0e4b",
    "permissions": ["read:summaries-info", "read:users-info"],
}

member_info = {
    "username": "testtwo@domain.com",
    "password": settings.test_member_password,
    "realm": "Username-Password-Authentication",
    "audience": settings.auth0_audience,
    "sub": "auth0|67c7664f657d0f4f7ac909a6",
    "permissions": [],
}


token_directory = {
    "jwt_test_token_member": member_info,
    "jwt_test_token_admin": admin_info,
}
