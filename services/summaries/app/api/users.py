from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, Security, BackgroundTasks

from app.api import crud
from app.dependencies import PermissionsValidator, validate_token

from app.models.tortoise import SummarySchema

# import pdb

from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)


from app.models.pydantic import (  # isort:skip
    UserResponseSchema,
    UserPayloadSchema,
    UserWithoutSummariesSchema,
)

router = APIRouter()

# member (current active user) routes


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=201,
)
async def create_user(
    payload: UserPayloadSchema, token: Annotated[dict, Security(validate_token)]
) -> UserResponseSchema:
    user_id = await crud.post_user(payload, token["sub"])
    response_object = {"id": user_id, "username": payload.username}
    return response_object


@router.get("/profile/", response_model=UserWithoutSummariesSchema)
async def read_current_active_user(
    token: Annotated[dict, Security(validate_token)],
) -> UserWithoutSummariesSchema:
    user = await crud.get_current_active_user(token["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    response_object = {
        "id": user["id"],
        "username": user["username"],
        "auth_sub": user["auth_sub"],
        "created_at": user["created_at"],
    }
    return response_object


@router.delete("/profile/", response_model=UserResponseSchema)
async def delete_current_active_user(
    token: Annotated[dict, Security(validate_token)],
) -> UserResponseSchema:
    user = await crud.get_current_active_user(token["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    await crud.delete_current_active_user(token["sub"])

    return user


# admin only routes
# 'permissions': ['read:users-info']


@router.get("/{id}/", response_model=UserWithoutSummariesSchema)
async def read_user(
    token: Annotated[dict, Security(PermissionsValidator(["read:users-info"]))],
    id: int = Path(..., gt=0),
) -> UserWithoutSummariesSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    response_object = {
        "id": user["id"],
        "username": user["username"],
        "auth_sub": user["auth_sub"],
        "created_at": user["created_at"],
    }
    return response_object


@router.get("/", response_model=List[UserWithoutSummariesSchema])
async def read_all_users(
    token: Annotated[dict, Security(PermissionsValidator(["read:users-info"]))],
) -> List[UserWithoutSummariesSchema]:
    users = await crud.get_all_users()
    if len(users) == 0:
        return users
    users = [
        {
            "id": user["id"],
            "username": user["username"],
            "auth_sub": user["auth_sub"],
            "created_at": user["created_at"],
        }
        for user in users
    ]
    return users


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(
    token: Annotated[dict, Security(PermissionsValidator(["read:users-info"]))],
    id: int = Path(..., gt=0),
) -> UserResponseSchema:
    user = await crud.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    await crud.delete_user(id)

    return user


# member routes
@router.post(
    "/profile/summaries/",
    response_model=SummaryResponseSchema,
    status_code=201,
)
async def create_current_active_user_summary(
    payload: SummaryPayloadSchema,
    background_tasks: BackgroundTasks,
    token: Annotated[dict, Security(validate_token)],
) -> SummaryResponseSchema:
    summary_id, user_id = await crud.post_current_active_user_summary(
        token["sub"], payload
    )
    background_tasks.add_task(generate_summary, summary_id, user_id, str(payload.query))
    response_object = {"id": summary_id, "query": payload.query, "user_id": user_id}
    return response_object


@router.get("/profile/summaries/", response_model=List[SummarySchema])
async def read_all_current_active_user_summaries(
    token: Annotated[dict, Security(validate_token)],
) -> List[SummarySchema]:
    return await crud.get_current_active_user_summaries(token["sub"])


@router.get("/profile/summaries/{id}/", response_model=SummarySchema)
async def read_current_active_user_summary(
    token: Annotated[dict, Security(validate_token)], id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.get_current_active_user_summary(id, token["sub"])
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.delete("/profile/summaries/{id}/", response_model=SummaryResponseSchema)
async def delete_current_active_user_summary(
    token: Annotated[dict, Security(validate_token)], id: int = Path(..., gt=0)
) -> SummaryResponseSchema:
    summary = await crud.get_current_active_user_summary(id, token["sub"])
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary_id, user_id = await crud.delete_current_active_user_summary(
        id, token["sub"]
    )
    as_dict = {"id": summary_id, "user_id": user_id, "query": summary.query}
    return as_dict


@router.put("/profile/summaries/{id}/", response_model=SummarySchema)
async def update_current_active_user_summary(
    payload: SummaryUpdatePayloadSchema,
    token: Annotated[dict, Security(validate_token)],
    id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.put_current_active_user_summary(id, token["sub"], payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


# admin 'permissions': ['read:summaries-info']
@router.get("/{user_id}/summaries/", response_model=List[SummarySchema])
async def read_all_summaries(
    token: Annotated[dict, Security(PermissionsValidator(["read:summaries-info"]))],
    user_id: int = Path(..., gt=0),
) -> List[SummarySchema]:
    return await crud.get_all_summaries(user_id)


@router.get("/{user_id}/summaries/{id}/", response_model=SummarySchema)
async def read_summary(
    token: Annotated[dict, Security(PermissionsValidator(["read:summaries-info"]))],
    user_id: int = Path(..., gt=0),
    id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.delete("/{user_id}/summaries/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(
    token: Annotated[dict, Security(PermissionsValidator(["read:summaries-info"]))],
    user_id: int = Path(..., gt=0),
    id: int = Path(..., gt=0),
) -> SummaryResponseSchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary_id, user_id = await crud.delete_summary(id, user_id)
    as_dict = {"id": summary_id, "user_id": user_id, "query": summary.query}
    return as_dict
