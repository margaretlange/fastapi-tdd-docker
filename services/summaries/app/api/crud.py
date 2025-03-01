# project/app/api/crud.py

from typing import List, Union, Tuple

from app.models.pydantic import SummaryPayloadSchema, UserPayloadSchema
from app.models.tortoise import TextSummary, User, SummarySchema
# import pdb


# summary crud
async def post_summary(user_id: int, payload: SummaryPayloadSchema) -> Tuple[int]:
    user = await User.get_or_none(id=user_id)
    summary = TextSummary(query=payload.query, summary="", user_id=user)
    await summary.save()
    return summary.id, summary.user_id.id


async def get_summary(id: int, user_id: int) -> Union[SummarySchema, None]:
    user = await User.get_or_none(id=user_id)
    summary = await TextSummary.filter(id=id, user_id=user).first()
    if summary:
        response = await SummarySchema.from_tortoise_orm(summary)
        return response
    return None


async def get_all_summaries(user_id: int) -> List[SummarySchema]:
    user = await User.get_or_none(id=user_id)
    summaries = await TextSummary.filter(user_id=user).all()
    summaries = [
        await SummarySchema.from_tortoise_orm(summary) for summary in summaries
    ]
    return summaries


async def delete_summary(id: int, user_id: int) -> Tuple[int]:
    user = await User.get_or_none(id=user_id)
    await TextSummary.filter(id=id, user_id=user).first().delete()
    return id, user.id


async def put_summary(
    id: int, user_id: int, payload: SummaryPayloadSchema
) -> Union[SummarySchema, None]:
    user = await User.get_or_none(id=user_id)
    summary = await TextSummary.filter(id=id, user_id=user).update(
        query=payload.query, summary=payload.summary
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id, user_id=user).first()
        response = await SummarySchema.from_tortoise_orm(updated_summary)
        return response
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
