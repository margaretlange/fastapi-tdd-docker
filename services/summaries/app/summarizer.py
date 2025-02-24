# project/app/summarizer.py

from assistant.graph import graph
from assistant.state import SummaryStateInput
import asyncio

from app.models.tortoise import TextSummary


async def generate_summary(summary_id: int, query: str) -> None:
    state = SummaryStateInput(research_topic=query)
    result = graph.invoke(state)
    await TextSummary.filter(id=summary_id).update(summary=result["running_summary"])
