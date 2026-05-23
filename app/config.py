from functools import lru_cache

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

    classifier_bucket: str = "fast"
    classifier_timeout_s: float = 30.0
    classifier_max_chars: int = 2000
    short_prompt_threshold: int = 80

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
