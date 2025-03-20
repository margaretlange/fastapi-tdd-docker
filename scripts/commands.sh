# helpful


# again
# normal run
docker-compose exec web python -m pytest

# disable warnings
docker-compose exec web python -m pytest -p no:warnings

# run only the last failed tests
docker-compose exec web python -m pytest --lf

# run only the tests with names that match the string expression
docker-compose exec web python -m pytest -k "summary and not test_read_summary"

# stop the test session after the first failure
docker-compose exec web python -m pytest -x

# enter PDB after first failure then end the test session
# this will save a lot of time
docker-compose exec web python -m pytest -x --pdb

# stop the test run after two failures

docker-compose exec web python -m pytest --maxfail=2

# show local variables in tracebacks
docker-compose exec web python -m pytest -l

# list the 2 slowest tests

docker-compose exec web python -m pytest --durations=2


docker-compose exec web python -m pytest tests/test_ping.py::test_pongprivate
docker-compose exec web python -m pytest tests/test_summaries_admin.py -x --pdb



docker-compose exec web isort --profile black .

# migrate db (file api only)
docker-compose -f docker-compose-api-only.yml exec web aerich init -t app.db.TORTOISE_ORM
docker-compose -f docker-compose-api-only.yml exec web aerich init-db 
docker-compose -f docker-compose-api-only-no-nginx.yml exec web aerich upgrade 
docker-compose exec web-db psql -U postgres

# server specific
# original docker compose
command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
new command
gunicorn --bind 0.0.0.0:8000 app.main:app -k uvicorn.workers.UvicornWorker --timeout=120

tortoise-cli
pip install tortoise-cli

docker-compose exec web tortoise-cli -c app.db.TORTOISE_ORM shell
