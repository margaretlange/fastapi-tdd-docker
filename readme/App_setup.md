- collect environment configuration variables and secrets
  - API_ENVIRONMENT is dev and NODE_ENV is development
  - CLIENT_ORIGIN_URL is "http://localhost:4040"
  - REACT_APP_AUTH0_CALLBACK_URL is "http://localhost:4040/callback"
  - API_URL is "http://localhost:8000"
  
  - test user and admin password should be strong passwords
  - for auth0 information, you will need to get it from the auth0 website in the settings of the test api application and the react application
   - WATCH_POLLING is true for development

- once you are done added all the configuration variables, add two test users to the auth0 tenant database
activate venv
python3 scripts/auth0_utils.py --create_users

- set up local environment files for api
(rename environment)
./services/summaries/setenv.sh > .env
add the JWT test tokens you have just generated

- set up local environment files for react
./services/client/setenv.sh > .env

- Set up local ssh key to pull the git deep researcher repository securely 
  - you must add this ssh key to your git account
- test back end only

docker-compose -f docker-compose-api-only-no-nginx.yml up --build -d
docker-compose -f docker-compose-api-only-no-nginx.yml exec web python -m pytest
docker-compose -f docker-compose-api-only-no-nginx.yml exec web python -m pytest --integration
docker-compose -f docker-compose-api-only-no-nginx.yml down

- test back end and front end together (gulp)

- docker-compose up --build -d
- initialize local db if not initialized already
   - kind of a pain
   - 
- Test it all out
I suggest tailing the web and client pods in separate windows
- try pinging just the public endpoint of the api from curl or the swagger docs tool. This should work and you should also see the request show up in the api pod logs

Now go to the website at 4040
Log in with your own account, then go give your admin privilege via the auth0 website.
Log in and log out

- Seed the database
  - edit the function seed_db in app/db.py in the api code. You'll need to get the ids for the users from the auth0 database on the auth0 website.
  - docker-compose exec web tortoise-cli -c app.db.TORTOISE_ORM shell
  - from app.db import seeddb
  - await 

Make a negligible change to the front end code and make sure react code refreshes. This is important for development.
