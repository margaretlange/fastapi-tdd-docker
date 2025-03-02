AUTH0_DOMAIN=https://dev-lhn1ufqgkgz8lk5w.us.auth0.com/oauth/token 
AUTH0_CLIENT_ID=u86kVPjj9Y5RxoSXgtJDvAXFOKTe5DPG
AUTH0_CLIENT_SECRET=yApiTedCGQ_LoKLgLFxplJMlRAPpcTbPni71cIsBjZSJBZ7gcTOs1XNaLqlhsM0m
AUTH0_AUDIENCE=https://hello-world.example.com

token=`/home/maggie/fastapi-tdd-docker/.github/request_auth0_token.sh $AUTH0_DOMAIN $AUTH0_CLIENT_ID $AUTH0_CLIENT_SECRET $AUTH0_AUDIENCE`
echo "AUTH0_ACCESS_TOKEN=$token" 
