from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"

    models: dict[str, str] = {
        "general":  "qwen3:30b-a3b",
        "coder":    "qwen2.5-coder:32b",
        "fast":     "qwen2.5:7b",
        "reasoner": "deepseek-r1:14b",
    }

    bucket_descriptions: dict[str, str] = {
        "general":  "everything else: knowledge, writing, brainstorming, summarising",
        "coder":    "programming, debugging, code review, software design, devops",
        "fast":     "short, simple, conversational, small talk",
        "reasoner": "math, multi-step logic, formal proofs, hard puzzles",
    }

    default_bucket: str = "general"
    classifier_bucket: str = "fast"
    classifier_timeout_s: float = 30.0
    classifier_max_chars: int = 2000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def _check(self):
        if not self.models:
            raise ValueError("MODELS must define at least one bucket")
        missing = set(self.models) - set(self.bucket_descriptions)
        if missing:
            raise ValueError(f"BUCKET_DESCRIPTIONS missing entries for: {sorted(missing)}")
        for name, bucket in [("DEFAULT_BUCKET", self.default_bucket),
                             ("CLASSIFIER_BUCKET", self.classifier_bucket)]:
            if bucket not in self.models:
                raise ValueError(f"{name}={bucket!r} is not a key in MODELS")
        return self
