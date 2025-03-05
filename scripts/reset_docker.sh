#!/usr/bin/bash

cd fastapi-tdd-docker
docker-compose down
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker system prune -a -f
