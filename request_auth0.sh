#!/usr/bin/bash

response=$(curl --request POST \
  --url https://dev-lhn1ufqgkgz8lk5w.us.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"u86kVPjj9Y5RxoSXgtJDvAXFOKTe5DPG","client_secret":"yApiTedCGQ_LoKLgLFxplJMlRAPpcTbPni71cIsBjZSJBZ7gcTOs1XNaLqlhsM0m","audience":"https://hello-world.example.com","grant_type":"client_credentials"}')
echo $response | jq -r .access_token
