Dockerfile.deploy
how to run it

api is run on port 8000 in the docker world
the client port is set as a variable PORT

docker build --file Dockerfile.deploy --tag fastdeploy "."

docker run -e DATABASE_URL=sqlite://sqlite.db -e DATABASE_TEST_URL=sqlite://sqlite.db -p 5003:8765 fastdeploy:latest

https://stackoverflow.com/questions/70288850/running-nginx-and-gunicorn-in-the-same-docker-file
https://dev-mus.medium.com/how-to-deploy-a-vite-react-app-using-nginx-server-d7190a29d8cd
