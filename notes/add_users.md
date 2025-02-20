docker-compose exec web aerich upgrade 
(when migration files exist)

check: 
docker-compose exec web-db psql -U postgres
\c web_dev
\dt

how do i add JUST the users tests
docker-compose exec web python -m pytest -p no:warnings -k "test_create_users_invalid_json"
docker-compose exec web python -m pytest -p no:warnings -k "users and users"

