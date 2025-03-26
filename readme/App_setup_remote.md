Github Actions (testing)

- add secrets to github
- add ssh key to the deep researcher repository
- trigger github actions test by making small change to main
- see if code passes


AWS ec2 (production)
- set up ec2 instance
  - log into bare instance and create an ssh key
  - add to github repository
  - run ansible playbook for ec2 to do the rest

 
- collect environment configuration variables and secrets

- set up environment for api
(rename environment)
./services/summaries/setenv.sh > .env

- set up environment for react
./services/summaries/setenv.sh > .env

run integration test on ec2 instance
- access postman 
