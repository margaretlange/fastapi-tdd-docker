Github Actions (testing)

- trigger github actions test by making small change to main
- see if code passes


AWS ec2 (production)
- set up ec2 instance
  - log into bare instance and create an ssh key
    - https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-22-04

  - add public key to github repository under personal settings
  - git clone git@github.com:margaretlange/fastapi-tdd-docker.git 
  - bash scripts/ec2.sh

- run init-letsencrypt.sh 
- collect environment configuration variables and secrets
(secrets_and_config_remote.txt)

- set up environment for production api
(rename environment)
./services/summaries/setenv.sh > .env

- set up environment for production react
./services/summaries/setenv.sh > .env

- make sure it's possible to get into postgres
- run commands in scripts/set_sshagent.sh
- migrate database
- access postman 
