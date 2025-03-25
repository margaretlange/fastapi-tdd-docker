- collect environment configuration variables and secrets
- add two test users to the auth0 tenant database
activate venv
python3 scripts/auth0_utils.py --create_users

- set up local environment for api
(rename environment)
./setenv.sh > .env

- set up local environment for react
./setenv.sh > .env

- testing locally environment

- add secrets to github
- trigger github actions test by making small change to main

- set up ec2 instance
  - log into bare instance and create an ssh key
  - add to github repository
  - run ansible playbook for ec2 to do the rest

 run integration test on ec2 instance
- access postman 
