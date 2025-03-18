from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.dependencies import validate_token

router = APIRouter()


@router.get("/status/")
async def status(settings: Settings = Depends(get_settings)):
    return {"status": "ok"}


@router.get("/status/private/", dependencies=[Depends(validate_token)])
async def status_private():
    return {"status": "This is a private endpoint."}


@router.get("/status/admin/", dependencies=[Depends(validate_token)])
async def status_admin():
    return {"status": "This is an admin endpoint."}
