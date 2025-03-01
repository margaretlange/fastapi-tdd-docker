# project/app/api/users.py
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path

from app.api import crud
from app.dependencies import validate_token
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)


# import pdb

from app.models.pydantic import (  # isort:skip
    UserResponseSchema,
    UserPayloadSchema,
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=201,
    dependencies=[Depends(validate_token)],
)
async def create_user(payload: UserPayloadSchema) -> UserResponseSchema:
    user_id = await crud.post_user(payload)

    response_object = {"id": user_id, "username": payload.username}
    return response_object


@router.get(
    "/{id}/", response_model=UserResponseSchema, dependencies=[Depends(validate_token)]
)
async def read_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    response_object = {"id": user["id"], "username": user["username"]}
    return response_object


@router.get(
    "/", response_model=List[UserResponseSchema], dependencies=[Depends(validate_token)]
)
async def read_all_users() -> List[UserResponseSchema]:
    users = await crud.get_all_users()
    if len(users) == 0:
        return users
    users = [{"id": user["id"], "username": user["username"]} for user in users]
    return users


@router.delete(
    "/{id}/", response_model=UserResponseSchema, dependencies=[Depends(validate_token)]
)
async def delete_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    await crud.delete_user(id)

    return user


@router.post(
    "/{user_id}/summaries/",
    response_model=SummaryResponseSchema,
    status_code=201,
    dependencies=[Depends(validate_token)],
)
async def create_summary(
    payload: SummaryPayloadSchema,
    background_tasks: BackgroundTasks,
    user_id: int = Path(..., gt=0),
) -> SummaryResponseSchema:
    # pdb.set_trace()
    summary_id, user_id = await crud.post_summary(user_id, payload)

    background_tasks.add_task(generate_summary, summary_id, user_id, str(payload.query))
    response_object = {"id": summary_id, "query": payload.query, "user_id": user_id}
    return response_object


@router.get(
    "/{user_id}/summaries/",
    response_model=List[SummarySchema],
    dependencies=[Depends(validate_token)],
)
async def read_all_summaries(user_id: int = Path(..., gt=0)) -> List[SummarySchema]:
    return await crud.get_all_summaries(user_id)


@router.get(
    "/{user_id}/summaries/{id}/",
    response_model=SummarySchema,
    dependencies=[Depends(validate_token)],
)
async def read_summary(
    user_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.delete(
    "/{user_id}/summaries/{id}/",
    response_model=SummaryResponseSchema,
    dependencies=[Depends(validate_token)],
)
async def delete_summary(
    user_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
) -> SummaryResponseSchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary_id, user_id = await crud.delete_summary(id, user_id)
    as_dict = {"id": summary_id, "user_id": user_id, "query": summary.query}
    return as_dict


@router.put(
    "/{user_id}/summaries/{id}/",
    response_model=SummarySchema,
    dependencies=[Depends(validate_token)],
)
async def update_summary(
    payload: SummaryUpdatePayloadSchema,
    id: int = Path(..., gt=0),
    user_id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.put_summary(id, user_id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
