uh oh using 
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/

Two tutorials
https://github.com/authlib/demo-oauth-client/blob/master/fastapi-google-login
in oath-tutorial-authlib
make sure to access http://127.0.0.1:8000 and not http://localhost:8000

and 

https://fastapi.tiangolo.com/tutorial/security/
in 
oath-tutorial-fastapi

Additional notes:
okay not possible with terraform (I hate you google)
this again:
https://blog.futuresmart.ai/integrating-google-authentication-with-fastapi-a-step-by-step-guide

https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform

https://medium.com/@himanshu.sharma.for.work/step-by-step-guide-to-implementing-oauth-authentication-in-fastapi-8291a3184f46

Notes on Oauth (oauth2)

https://en.wikipedia.org/wiki/OAuth
OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.

https://fastapi.tiangolo.com/tutorial/security/first-steps/#create-mainpy
But in this case, the same FastAPI application will handle the API and the authentication.
In this example we are going to use OAuth2, with the Password flow, using a Bearer token. We do that using the OAuth2PasswordBearer class.

When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.

OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.

The spec also says that the client can send another form field "scope".

JWT = Json web tokens
Tokens and password hashing are two different components.

# openssl rand -hex 32
how to get your password salt (is it a salt?)

The important thing to keep in mind is that the sub key should have a unique identifier across the entire application, and it should be a string.

If you open the developer tools, you could see how the data sent only includes the token, the password is only sent in the first request to authenticate the user and get that access token, but not afterwards


https://medium.com/@vivekpemawat/enabling-googleauth-for-fast-api-1c39415075ea

in google auth client make sure to put
http://127.0.0.1:8000/auth
in client redirect list


OpenAPI security scheme


okay more on this
https://developer.auth0.com/resources/labs/authentication/google-social-connection-to-login#introduction
also looking at finances wiki

i'm putting the secret into terraform plain text should fix later
https://blog.fahhem.com/2024/01/terraform-gcp-2024/
