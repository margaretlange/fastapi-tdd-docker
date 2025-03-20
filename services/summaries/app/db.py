# project/app/db.py

import logging  # new
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async  # new
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")  # new


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


# new
async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


# this doesn't work
# async def seed_db() -> None:
#    await Tortoise.init(
#        db_url=os.environ.get("DATABASE_URL"),
#        modules={"models": ["models.tortoise", "aerich.models"]},
#    )
#    print(await post_user({'username': 'Margaret Lange'}, 'google-oauth2|106169556027978612521'))
#    print(await post_user({'username': 'testtwo@domain.com'}, 'auth0|67c7664f657d0f4f7ac909a6'))
#    await Tortoise.close_connections()

# new
if __name__ == "__main__":
    # pass
    run_async(generate_schema())
