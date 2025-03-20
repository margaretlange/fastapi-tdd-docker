from app.api.crud import post_user
from app.models.pydantic import UserPayloadSchema


ml=UserPayloadSchema(**{'username': 'Margaret Lange'})
await post_user(ml, 'google-oauth2|106169556027978612521')
test=UserPayloadSchema(**{'username': 'testtwo@domain.com'})
await post_user(test, 'auth0|67c7664f657d0f4f7ac909a6')


