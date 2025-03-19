from app.config import settings

admin_info = {
        "username": "adminlady@domain.com",
        "password": settings.test_admin_password,
        "realm": "Username-Password-Authentication",
        "audience": settings.auth0_audience,
    }

member_info = {
        "username": "testtwo@domain.com",
        "password": settings.test_member_password,
        "realm": "Username-Password-Authentication",
        "audience": settings.auth0_audience,
    }


token_directory = {'jwt_test_token_member': member_info, 'jwt_test_token_admin': admin_info}
