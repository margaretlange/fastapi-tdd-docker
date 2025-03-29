
# docker login ghcr.io -u margaretlange -p ${GITHUB_TOKEN}
# docker pull ghcr.io/margaretlange/fastapi-tdd-docker/summarizer@sha256:f51ff8860f1a66f82e576c7cd81de6b5e7819b8fbfb34219917e763f2861321d
docker run -d \
--name github \
-e PORT=8765 \
-e ENVIRONMENT=dev \
-e DATABASE_URL=sqlite://sqlite.db \
-e DATABASE_TEST_URL=sqlite://sqlite.db \
-e JWT_TEST_ENCODE_KEY=$JWT_TEST_ENCODE_KEY \
-p 5003:8765 \
ghcr.io/margaretlange/fastapi-tdd-docker/summarizer:latest
# docker exec fastapi-tdd python -m pytest . 
# docker exec fastapi-tdd python -m pip freeze > output.txt

