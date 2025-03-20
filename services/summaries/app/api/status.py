from fastapi import APIRouter, Depends, Security

from app.config import Settings, get_settings
from app.dependencies import validate_token, PermissionsValidator

router = APIRouter()


@router.get("/status/")
async def status(settings: Settings = Depends(get_settings)):
    return {"status": "ok"}


@router.get("/status/private/", dependencies=[Depends(validate_token)])
async def status_private():
    return {"status": "This is a private endpoint."}


@router.get("/status/admin/", dependencies=[Security(PermissionsValidator(["read:summaries-info"]))])
async def status_admin():
    return {"status": "This is an admin endpoint."}
