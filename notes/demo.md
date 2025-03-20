how to turn on the api for the demo

Check the following are up to date
tavily api
openai api
ssl cert
domain

cd ec2_scripts
./ec2_ls
./ec2_ssh [id]

get fresh keys by running scripts/auth0_utils with command in invocation file
paste into postman

if not up:
run the contents of set_sshagent.sh
docker-compose -f docker-compose-api-only.yml up --build -d
reset docker if running out of memory

test postman endpoints public and private
then test substantive endpoints
