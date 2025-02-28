# project/app/api/users.py
from typing import List
import pdb
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


@router.get("/{id}/", response_model=UserResponseSchema)
async def read_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    response_object = {"id": user['id'], "username": user['username']}
    return response_object


@router.get("/", response_model=List[UserResponseSchema])
async def read_all_users() -> List[UserResponseSchema]:
    users = await crud.get_all_users()
    if len(users) == 0:
        return users
    users = [{"id": user['id'], "username": user['username']} for user in users]
    return users

@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    await crud.delete_user(id)

    return user
