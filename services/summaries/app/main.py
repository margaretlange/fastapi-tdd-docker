# project/app/main.py


import logging

from fastapi import FastAPI

from app.api import ping, users
from app.db import init_db

# from app.config import get_settings

# from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    # settings = get_settings()
    # application.add_middleware(
    #    CORSMiddleware,
    #    allow_origins=[settings.client_origin_url],
    #    allow_methods=["*"],
    #    allow_headers=["Authorization", "Content-Type"],
    #    max_age=86400,
    # )

    application.include_router(ping.router)
    application.include_router(users.router, prefix="/users", tags=["users"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
