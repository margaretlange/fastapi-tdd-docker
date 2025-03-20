On calling external apis:

To run the tests without hitting the auth0 api:
docker-compose exec web python -m pytest 

To run the tests with hitting the auth0 api:
docker-compose exec web python -m pytest --integration

On openapi and tavily:
None of the current tests actually call tavily or openapi.
