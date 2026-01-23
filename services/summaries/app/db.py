# project/app/db.py

import logging  # new
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async  # new
from tortoise.contrib.fastapi import register_tortoise

from app.api.crud import post_current_active_user_summary, post_user
from app.models.pydantic import SummaryPayloadSchema, UserPayloadSchema
from app.summarizer import generate_summary

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
    log.info("Initializing database at %s..." % os.environ.get("DATABASE_URL"))
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
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


# trying to run this from the tortoise shell
async def seed_db() -> None:
    ml = UserPayloadSchema(**{"username": "Margaret Lange"})
    await post_user(ml, "google-oauth2|106169556027978612521")
    test = UserPayloadSchema(**{"username": "testtwo@domain.com"})
    await post_user(test, "auth0|67c7664f657d0f4f7ac909a6")
    # Trying some summary code next
    # cd_payload = SummaryPayloadSchema(query="Who was Charles Darwin?")
    # al_payload = SummaryPayloadSchema(query="Who was Ada Lovelace?")
    # acd_payload = SummaryPayloadSchema(query="Who was Arthur Conan Doyle?")
    # summary_id, user_id = await post_current_active_user_summary(
    #    "google-oauth2|106169556027978612521", cd_payload
    # )
    # await generate_summary(summary_id, user_id, str(cd_payload.query))
    #summary_id, user_id = await post_current_active_user_summary(
    #    "google-oauth2|106169556027978612521", al_payload
    #)
    #await generate_summary(summary_id, user_id, str(al_payload.query))
    #summary_id, user_id = await post_current_active_user_summary(
    #    "auth0|67c7664f657d0f4f7ac909a6", acd_payload
    #)
    #await generate_summary(summary_id, user_id, str(acd_payload.query))


# new
if __name__ == "__main__":
    # pass
    run_async(generate_schema())
