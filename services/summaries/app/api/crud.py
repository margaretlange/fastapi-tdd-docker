# project/app/api/crud.py

from typing import List, Union

from app.models.pydantic import UserPayloadSchema
from app.models.tortoise import User

# from typing import Tuple


# import pdb

# user crud

# current user


async def post_user(payload: UserPayloadSchema, auth_sub: str) -> int:
    user = User(username=payload.username, auth_sub=auth_sub)
    await user.save()
    return user.id


async def get_user(id: int) -> Union[dict, None]:
    user = await User.filter(id=id).first().values()
    if user:
        return user
    return None


async def get_current_active_user(auth_sub: str) -> Union[dict, None]:
    user = await User.filter(auth_sub=auth_sub).first().values()
    if user:
        return user
    return None


async def get_all_users() -> List:
    users = await User.all().values()
    return users


async def delete_current_active_user(auth_sub: str) -> int:
    user = await User.filter(auth_sub=auth_sub).first().delete()
    return user


async def delete_user(id: int) -> int:
    user = await User.filter(id=id).first().delete()
    return user


# summary crud
# async def post_current_active_user_summary(auth_sub: str, payload: SummaryPayloadSchema) -> Tuple[int]:
#     user = await User.get_or_none(auth_sub=auth_sub)
#     summary = TextSummary(query=payload.query, summary="", user=user)
#     await summary.save()
#     return summary.id, summary.user_id.id


# async def get_summary(id: int, user_id: int) -> Union[SummarySchema, None]:
#     user = await User.get_or_none(id=user_id)
#     summary = await TextSummary.filter(id=id, user=user).first()
#     if summary:
#         response = await SummarySchema.from_tortoise_orm(summary)
#         return response
#     return None


# async def get_current_active_user_summary(id: int, auth_sub: str) -> Union[SummarySchema, None]:
#     user = await User.get_or_none(auth_sub=auth_sub)
#     summary = await TextSummary.filter(id=id, user=user).first()
#     if summary:
#         response = await SummarySchema.from_tortoise_orm(summary)
#         return response
#     return None


# async def get_all_summaries(user_id: int) -> List[SummarySchema]:
#     user = await User.get_or_none(id=user_id)
#     summaries = await TextSummary.filter(user=user).all()
#     summaries = [
#         await SummarySchema.from_tortoise_orm(summary) for summary in summaries
#     ]
#     return summaries


# async def get_current_active_user_summaries(auth_sub: str) -> List[SummarySchema]:
#     user = await User.get_or_none(auth_sub=auth_sub)
#     summaries = await TextSummary.filter(user=user).all()
#     summaries = [
#         await SummarySchema.from_tortoise_orm(summary) for summary in summaries
#     ]
#     return summaries


# async def delete_current_active_user_summary(auth_sub: str, user: int) -> Tuple[int]:
#     user = await User.get_or_none(auth_sub=auth_sub)
#     await TextSummary.filter(id=id, user=user).first().delete()
#     return id, user.id


# async def put_current_active_user_summary(
#     id: int, auth_sub: str, payload: SummaryPayloadSchema
# ) -> Union[SummarySchema, None]:
#     user = await User.get_or_none(auth_sub=auth_sub)
#     summary = await TextSummary.filter(id=id, user_id=user).update(
#         query=payload.query, summary=payload.summary
#     )
#     if summary:
#         updated_summary = await TextSummary.filter(id=id, user_id=user).first()
#         response = await SummarySchema.from_tortoise_orm(updated_summary)
#         return response
#     return None
