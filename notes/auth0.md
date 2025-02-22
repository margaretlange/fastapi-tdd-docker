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
