# project/app/api/summaries.py

from typing import List

from fastapi import BackgroundTasks, HTTPException, Path

from app.api import crud
from app.api.users import router
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)
import pdb


@router.post(
    "/{user_id}/summaries/", response_model=SummaryResponseSchema, status_code=201
)
async def create_summary(
    payload: SummaryPayloadSchema,
    background_tasks: BackgroundTasks,
    user_id: int = Path(..., gt=0),
) -> SummaryResponseSchema:
    summary_id, user_id = await crud.post_summary(user_id, payload)

    background_tasks.add_task(generate_summary, summary_id, user_id, str(payload.query))
    response_object = {"id": summary_id, "query": payload.query, "user_id": user_id}
    return response_object


@router.get("/{user_id}/summaries/", response_model=List[SummarySchema])
async def read_all_summaries(user_id: int = Path(..., gt=0)) -> List[SummarySchema]:
    return await crud.get_all_summaries(user_id)


@router.get("/{user_id}/summaries/{id}/", response_model=SummarySchema)
async def read_summary(
    user_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
) -> SummarySchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.delete("/{user_id}/summaries/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(
    user_id: int = Path(..., gt=0), id: int = Path(..., gt=0)
) -> SummaryResponseSchema:
    summary = await crud.get_summary(id, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary = await crud.delete_summary(id, user_id)
    return summary


@router.put("/{user_id}/summaries/{id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema,
    id: int = Path(..., gt=0),
    user_id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.put_summary(id, user_id, payload)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
