from dataclasses import asdict
from typing import Any, AsyncIterator

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .config import Settings
from .ollama import OllamaClient
from .routing import RouterDecision, route

router = APIRouter()


def get_ollama(request: Request) -> OllamaClient:
    return request.app.state.ollama


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


@router.get("/healthcheck")
async def healthcheck(
    ollama: OllamaClient = Depends(get_ollama),
    settings: Settings = Depends(get_settings),
):
    return {"ok": await ollama.healthy(), "ollama": settings.ollama_url}


@router.get("/v1/models")
async def list_models(settings: Settings = Depends(get_settings)):
    ids = ["auto", *settings.models.keys(), *settings.models.values()]
    return {"object": "list", "data": [{"id": i, "object": "model"} for i in ids]}


@router.post("/v1/chat/completions")
async def chat_completions(
    request: Request,
    ollama: OllamaClient = Depends(get_ollama),
    settings: Settings = Depends(get_settings),
):
    body: dict[str, Any] = await request.json()
    decision = await _resolve_decision(body, ollama, settings)
    body["model"] = decision.model

    if not body.get("stream"):
        response = await ollama.chat(body)
        payload = response.json()
        payload["x_router"] = asdict(decision)
        return JSONResponse(payload, status_code=response.status_code)

    async def event_stream() -> AsyncIterator[bytes]:
        yield (
            f": routed bucket={decision.bucket} "
            f"model={decision.model} source={decision.source}\n\n"
        ).encode()
        async with ollama.stream_chat(body) as response:
            async for chunk in response.aiter_raw():
                yield chunk

    return StreamingResponse(event_stream(), media_type="text/event-stream")


async def _resolve_decision(
    body: dict[str, Any],
    ollama: OllamaClient,
    settings: Settings,
) -> RouterDecision:
    requested = body.get("model", "auto")
    if requested == "auto":
        return await route(
            body.get("messages", []),
            ollama=ollama,
            models=settings.models,
            classifier_model=settings.models[settings.classifier_bucket],
            short_threshold=settings.short_prompt_threshold,
            classifier_max_chars=settings.classifier_max_chars,
            classifier_timeout=settings.classifier_timeout_s,
        )
    if requested in settings.models:
        return RouterDecision(
            bucket=requested, model=settings.models[requested], source="explicit"
        )
    return RouterDecision(bucket="manual", model=requested, source="explicit")
