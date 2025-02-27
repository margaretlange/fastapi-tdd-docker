# project/app/api/users.py
from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.tortoise import UserSchema
# import pdb

from app.models.pydantic import (  # isort:skip
    UserResponseSchema,
    UserPayloadSchema,
)


router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(payload: UserPayloadSchema) -> UserResponseSchema:
    user_id = await crud.post_user(payload)

    response_object = {"id": user_id, "username": payload.username}
    return response_object


@router.get("/{id}/", response_model=UserSchema)
async def read_user(id: int = Path(..., gt=0)) -> UserSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.get("/", response_model=List[UserSchema])
async def read_all_users() -> List[UserSchema]:
    return await crud.get_all_users()


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    await crud.delete_user(id)

    return user
