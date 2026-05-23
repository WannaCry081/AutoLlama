import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api import router
from app.config import Settings
from app.ollama import OllamaClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )
    async with httpx.AsyncClient(timeout=None) as http:
        app.state.settings = settings
        app.state.ollama = OllamaClient(settings.ollama_url, http)
        logging.getLogger(__name__).info(
            "router up — ollama=%s classifier_bucket=%s",
            settings.ollama_url, settings.classifier_bucket,
        )
        yield


app = FastAPI(title="Ollama Auto Router", version="0.1.0", lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    settings = Settings()
    uvicorn.run("main:app", host=settings.host, port=settings.port, log_level=settings.log_level)
