from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .routing import RouterDecision, route

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(request: Request):
    ollama = request.app.state.ollama
    settings = request.app.state.settings
    return {"ok": await ollama.healthy(), "ollama": settings.ollama_url}


@router.get("/v1/models")
async def list_models(request: Request):
    models = request.app.state.settings.models
    ids = ["auto", *models.keys(), *models.values()]
    return {"object": "list", "data": [{"id": i, "object": "model"} for i in ids]}


@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    ollama = request.app.state.ollama
    settings = request.app.state.settings
    body: dict[str, Any] = await request.json()

    requested = body.get("model", "auto")
    if requested == "auto":
        decision = await route(body.get("messages", []), ollama, settings)
    elif requested in settings.models:
        decision = RouterDecision(requested, settings.models[requested], "explicit")
    else:
        decision = RouterDecision("manual", requested, "explicit")

    body["model"] = decision.model

    if not body.get("stream"):
        response = await ollama.chat(body)
        payload = response.json()
        payload["x_router"] = asdict(decision)
        return JSONResponse(payload, status_code=response.status_code)

    async def event_stream():
        yield (
            f": routed bucket={decision.bucket} "
            f"model={decision.model} source={decision.source}\n\n"
        ).encode()
        async with ollama.stream_chat(body) as response:
            async for chunk in response.aiter_raw():
                yield chunk

    return StreamingResponse(event_stream(), media_type="text/event-stream")
