why can't i migrate my database(s) properly?

Seeding the database
https://fastapi.tiangolo.com/advanced/events/#lifespan-function

re: gunicorn
I think there is only one place where we add an additional path, and it's the current working directory. I think this was done to make it easy for people to deploy without putting their code in a proper package. That code lives here:
https://github.com/benoitc/gunicorn/issues/2466

why my imports work, I guess

tortoise-cli is working
pip3 install tortoise-cli
docker-compose exec web tortoise-cli -c app.db.TORTOISE_ORM shell

