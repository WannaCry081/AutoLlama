import logging
from dataclasses import dataclass
from typing import Any

from .constants import (
    CLASSIFIER_PROMPT,
    CODE_HINTS,
    DEFAULT_BUCKET,
    REASON_HINTS,
)
from .ollama import OllamaClient

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RouterDecision:
    bucket: str
    model: str
    source: str  # heuristic | classifier | explicit


def extract_user_text(messages: list[dict[str, Any]]) -> str:
    for message in reversed(messages):
        if message.get("role") != "user":
            continue
        content = message.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return " ".join(
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            )
    return ""


def heuristic_bucket(text: str, short_threshold: int) -> str | None:
    if not text.strip():
        return "fast"
    if CODE_HINTS.search(text):
        return "coder"
    if REASON_HINTS.search(text):
        return "reasoner"
    if len(text) < short_threshold:
        return "fast"
    return None


async def classify_with_llm(
    ollama: OllamaClient,
    classifier_model: str,
    text: str,
    buckets: list[str],
    *,
    max_chars: int,
    timeout: float,
) -> str:
    try:
        answer = await ollama.generate(
            model=classifier_model,
            prompt=CLASSIFIER_PROMPT.format(prompt=text[:max_chars]),
            timeout=timeout,
            temperature=0,
            num_predict=8,
        )
    except Exception as exc:
        log.warning("classifier failed, defaulting to %s: %s", DEFAULT_BUCKET, exc)
        return DEFAULT_BUCKET

    answer = answer.strip().lower()
    for bucket in buckets:
        if bucket in answer:
            return bucket
    return DEFAULT_BUCKET


async def route(
    messages: list[dict[str, Any]],
    *,
    ollama: OllamaClient,
    models: dict[str, str],
    classifier_model: str,
    short_threshold: int,
    classifier_max_chars: int,
    classifier_timeout: float,
) -> RouterDecision:
    text = extract_user_text(messages)

    bucket = heuristic_bucket(text, short_threshold)
    if bucket is not None:
        source = "heuristic"
    else:
        bucket = await classify_with_llm(
            ollama,
            classifier_model,
            text,
            list(models.keys()),
            max_chars=classifier_max_chars,
            timeout=classifier_timeout,
        )
        source = "classifier"

    decision = RouterDecision(bucket=bucket, model=models[bucket], source=source)
    log.info("routed bucket=%s model=%s source=%s", decision.bucket, decision.model, decision.source)
    return decision
