# project/app/api/crud.py

from typing import List, Union

from app.models.pydantic import SummaryPayloadSchema, UserPayloadSchema
from app.models.tortoise import TextSummary, User


# summary crud
async def post_summary(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(query=payload.query, summary="", user_id=payload.user_id)
    await summary.save()
    return summary.id, summary.user_id


async def get_summary(id: int, user_id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id, user_id=user_id).first().values()
    if summary:
        return summary
    return None


async def get_all_summaries(user_id: int) -> List:
    summaries = await TextSummary.all(user_id=user_id).values()
    return summaries


async def delete_summary(id: int, user_id: int) -> int:
    summary = await TextSummary.filter(id=id, user_id=user_id).first().delete()
    return summary


async def put_summary(id: int, user_id: int, payload: SummaryPayloadSchema) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id, user_id=user_id).update(
        query=payload.query, summary=payload.summary
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id, user_id=user_id).first().values()
        return updated_summary
    return None


# user crud
async def post_user(payload: UserPayloadSchema) -> int:
    user = User(username=payload.username)
    await user.save()
    return user.id


async def get_user(id: int) -> Union[dict, None]:
    user = await User.filter(id=id).first().values()
    if user:
        return user
    return None


async def get_all_users() -> List:
    users = await User.all().values()
    return users


async def delete_user(id: int) -> int:
    user = await User.filter(id=id).first().delete()
    return user
