react version 6
react v18+
what is node requirement?
at least 20. so upgraded to 20.

resetting up the api_fastapi project
back at it

tutorials:
spa_react_javascript_hello-world
https://developer.auth0.com/resources/guides/spa/react/basic-authentication

api_fastapi_python_hello-world
https://developer.auth0.com/resources/code-samples/api/fastapi/basic-authorization

01-starting-project tutorial
so what form of authenication is my spa using?
Universal Login?

https://dev-lhn1ufqgkgz8lk5w.us.auth0.com/authorize?
  response_type=code|token&
  client_id=jxxjVmPI6dHQf0JJanyJS0CcFb8udXip&
  connection={connectionName}&
  redirect_uri=http://localhost:4040/callback&
  state={state}

this seems useful too
https://testdriven.io/blog/fastapi-react/

did i not have this problem b4 because of nginx
I think i didn't have any calls
https://stackoverflow.com/questions/77060233/unknown-host-error-calling-containerized-backend-from-frontend


CLIENT_ORIGIN_URL=http://localhost:4040
REACT_APP_API_SERVER_URL=http://localhost:8000

for hot reloading
WATCHPACK_POLLING=true
in .env file
