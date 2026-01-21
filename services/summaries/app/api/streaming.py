from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.config import get_settings, Settings

import asyncio

router = APIRouter()


async def text_streamer():
    print("start streaming")
    test_message = "A test message for text streaming"
    for token in test_message.split():
        yield str(token)
        await asyncio.sleep(1)


@router.post("/streaming")
def text_completions(settings: Settings = Depends(get_settings)):
    return StreamingResponse(text_streamer())
