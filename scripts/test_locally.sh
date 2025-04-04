docker stop fastapi-tdd
docker rm fastapi-tdd
docker build \
       --tag testingapi:latest \
       --file ./services/summaries/Dockerfile.prod \
       "./services/summaries"

docker run -d \
--name fastapi-tdd \
-e PORT=8765 \
-e ENVIRONMENT=dev \
-e DATABASE_URL=sqlite://sqlite.db \
-e DATABASE_TEST_URL=sqlite://sqlite.db \
-e JWT_TEST_ENCODE_KEY=$JWT_TEST_ENCODE_KEY \
-p 5003:8765 \
testingapi:latest

docker exec fastapi-tdd python -m pytest .
docker cp fastapi-tdd:/home/app/web/requirement_freeze.txt ./services/summaries/requirement_freeze.txt

docker stop fastapi-tdd
docker rm fastapi-tdd

