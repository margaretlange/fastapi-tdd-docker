# project/app/api/ping.py


from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.dependencies import validate_token

router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "environment": settings.environment,
        "testing": settings.testing,
    }


@router.get("/ping/private", dependencies=[Depends(validate_token)])
async def pongprivate():
    return {"ping": "This is a private endpoint"}
