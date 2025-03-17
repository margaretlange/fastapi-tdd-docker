# project/app/summarizer.py

import logging

from assistant.graph import graph
from assistant.state import SummaryStateInput

from app.models.tortoise import TextSummary

# import asyncio


async def generate_summary(summary_id: int, user_id: int, query: str) -> None:
    state = SummaryStateInput(research_topic=query)
    logging.warning("Before graph invoke in generate_summary")
    result = graph.invoke(state)
    logging.warning("After graph invoke in generate_summary")
    await TextSummary.filter(id=summary_id, user_id=user_id).update(
        summary=result["running_summary"]
    )
