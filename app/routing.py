import logging
from dataclasses import dataclass
from typing import Any

from .ollama import OllamaClient

log = logging.getLogger(__name__)


@dataclass
class RouterDecision:
    bucket: str
    model: str
    source: str  # classifier | default | explicit


CLASSIFIER_PROMPT = """\
You are a request router. Classify the user's prompt into ONE bucket.
Reply with exactly one lowercase word, no punctuation, no explanation:

{buckets}

User prompt:
\"\"\"{prompt}\"\"\"

One word:"""


def build_classifier_prompt(descriptions: dict[str, str], prompt: str) -> str:
    width = max(len(name) for name in descriptions)
    buckets = "\n".join(f"- {n.ljust(width)} : {d}" for n, d in descriptions.items())
    return CLASSIFIER_PROMPT.format(buckets=buckets, prompt=prompt)


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


async def route(messages, ollama: OllamaClient, settings) -> RouterDecision:
    text = extract_user_text(messages).strip()
    models = settings.models
    descriptions = settings.bucket_descriptions
    default = settings.default_bucket

    if not text:
        return _decide(default, models, "default")

    prompt = build_classifier_prompt(descriptions, text[: settings.classifier_max_chars])
    try:
        answer = await ollama.generate(
            model=models[settings.classifier_bucket],
            prompt=prompt,
            timeout=settings.classifier_timeout_s,
            temperature=0,
            num_predict=8,
        )
    except Exception as exc:
        log.warning("classifier failed, defaulting to %s: %s", default, exc)
        return _decide(default, models, "default")

    answer = answer.strip().lower()
    bucket = next((b for b in descriptions if b in answer), default)
    return _decide(bucket, models, "classifier")


def _decide(bucket: str, models: dict[str, str], source: str) -> RouterDecision:
    decision = RouterDecision(bucket=bucket, model=models[bucket], source=source)
    log.info("routed bucket=%s model=%s source=%s", bucket, decision.model, source)
    return decision
