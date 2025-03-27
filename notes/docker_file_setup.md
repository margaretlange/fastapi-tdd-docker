Dockerfile.deploy
how to run it

api is run on port 8000 in the docker world
the client port is set as a variable PORT

docker build --file Dockerfile.deploy --tag fastdeploy "."

docker run -e DATABASE_URL=sqlite://sqlite.db -e DATABASE_TEST_URL=sqlite://sqlite.db -p 5003:8765 fastdeploy:latest

https://stackoverflow.com/questions/70288850/running-nginx-and-gunicorn-in-the-same-docker-file
https://dev-mus.medium.com/how-to-deploy-a-vite-react-app-using-nginx-server-d7190a29d8cd

# run tests as in github

docker build \
       --tag testingapi:latest \
       --file ./services/summaries/Dockerfile.prod \
       "./services/summaries"

docker run \
--name fastapi-tdd \
-e PORT=8765 \
-e ENVIRONMENT=dev \
-e DATABASE_URL=sqlite://sqlite.db \
-e DATABASE_TEST_URL=sqlite://sqlite.db \
-e JWT_TEST_ENCODE_KEY=$JWT_TEST_ENCODE_KEY \
-p 5003:8765 \
testingapi:latest


docker run \
--name fastapi-tdd \
-e PORT=8765 \
-e ENVIRONMENT=dev \
-e OPENAI_API_KEY=$OPENAI_API_KEY \
-e TAVILY_API_URL=$TAVILY_API_KEY  \
-e DATABASE_URL=sqlite://sqlite.db \
-e DATABASE_TEST_URL=sqlite://sqlite.db \
-e AUTH0_AUDIENCE=$AUTH0_AUDIENCE \
-e AUTH0_DOMAIN=$AUTH0_DOMAIN \
-e AUTH0_CLIENT_ID=$TEST_AUTH0_CLIENT_ID \
-e AUTH0_CLIENT_SECRET=$TEST_AUTH0_CLIENT_SECRET \
-e TEST_ADMIN_PASSWORD=$AUTH0_TEST_ADMIN_PASSWORD" \
-e TEST_MEMBER_PASSWORD=$AUTH0_TEST_MEMBER_PASSWORD \
-e JWT_TEST_ENCODE_KEY=$JWT_TEST_ENCODE_KEY \
-p 5003:8765 \
testingapi:latest


docker exec fastapi-tdd python -m pytest .

