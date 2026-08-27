"""
SSE endpoint: runs the content pipeline and streams one event per
agent as it finishes.

Register in app/main.py with:
    from app.api import routes_content_stream
    app.include_router(routes_content_stream.router)
"""

import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agents.orchestrator import run_pipeline

router = APIRouter()


class BusinessInput(BaseModel):
    business_name: str
    business_type: str
    target_audience: str
    platform: str
    location: str
    revenue_band: str


def _sse_format(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


@router.post("/api/content/stream")
async def stream_content(payload: BusinessInput):
    async def event_generator():
        async for event in run_pipeline(payload.model_dump()):
            yield _sse_format(event)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
