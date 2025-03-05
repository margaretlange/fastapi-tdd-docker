auth0 terraform attempts
https://registry.terraform.io/providers/auth0/auth0/latest/docs/guides/quickstart
only one provider per module

With Auth0, you can define sources of users, otherwise known as connections, which may include identity providers (such as Google or LinkedIn), databases, or passwordless authentication methods.

giving up on terraform for now
maybe after trying this out:
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
auth0-example

Looks like I have to make an api first
my domain is [tenant-name].us.auth0.com

tenant
application (client)
api (terraform resource server)
connections: database, google, github etc

https://github.com/margaretlange/auth0-python-fastapi-sample
i guess my endpoint is secret?

I think I should read this:
https://developer.auth0.com/resources/guides/spa/react/basic-authentication/v17-javascript-react-router-5

I could even try pairing with this
https://github.com/auth0-developer-hub/api_fastapi_python_hello-world/blob/main/README.md

"You first integrate your React application with Auth0. Your application will then redirect users to an Auth0 customizable login page when they need to log in. Once your users log in successfully, Auth0 redirects them back to your React app, returning JSON Web Tokens (JWTs) with their authentication and user information."

okay i'm going to delete my api object for now maybe recreate later with terraform if needed?

React Tutorial
(using v5 router? but also there's a v6 router option)
looks like i will create an auth0 application using this tutorial

"In Security StackExchange, Conor Mancone explains that server-side guards are about protecting data while client-side guards are about improving user experience."
https://security.stackexchange.com/questions/221277/how-good-are-angular-route-guards-from-a-security-standpoint/221281#221281

spa_react-v17_javascript_hello-world_react-router-5
now setting up the api

slightly different tutorial
https://developer.auth0.com/resources/code-samples/api/fastapi/basic-authorization

If you are using this API with any of the compatible Hello World client applications, you can skip this section. Your client application will get an access token from Auth0 and use it to make authenticated requests to your API.

api_fastapi_python_hello-world
okay have both apps on screen next wow

The value of the Auth0 Audience must be the same for both the React client application and the API server you decided to set up.

smaller hello world is in folder auth0-example

Notes on smaller v larger auth0 example for 30 mins:
config.py very similar
small[utils.py] = large[custom_exceptions.py + json_web_token.py]

https://www.reddit.com/r/webdev/comments/v8bkqe/what_would_be_the_best_way_to_collect_additional/

how to generate token with sdk
test_auth0_sdk

What accounts do I currently have on auth0?

auth0 tenant (identified with autho domain)
auth0 application (identified with a client_id and client_secret; specific to frontend, you would have a mobile app and web app application for same backend)

applications come with login logout.  you have to set an audience api value to get tokens? 

is the audience api your actual api URL on the web?

so you get a test application api automatically when you create an api (at least through the dashboard)

enable password grant for client?
https://auth0.com/docs/get-started/applications/update-grant-types
under "advanced settings" kill me now

auth0.exceptions.Auth0Error: 400: Connection must be enabled for this client to perform single user creation and signup operations

Dashboard → Authentication → Database → Username-Password- Authentication → Applications tab and selecting your M2M application from there. 

wondering if i can use a security class
https://fastapi.tiangolo.com/reference/security/

not enough i don't think. see here:
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
wrap in security?

https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
In some cases you don't really need the return value of a dependency inside your path operation function.

Or the dependency doesn't return a value.

But you still need it to be executed/solved.

okay then I can put it in path operation function
just do users for now, try to comment out everything else.

going through this again https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/ with greater knowledge

Declare a FastAPI Security dependency.

The only difference with a regular dependency is that it can declare OAuth2 scopes that will be integrated with OpenAPI and the automatic UI docs (by default at /docs).
