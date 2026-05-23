from typing import Any

import httpx


class OllamaClient:
    def __init__(self, base_url: str, http: httpx.AsyncClient) -> None:
        self._base = base_url.rstrip("/")
        self._http = http

    async def generate(self, model: str, prompt: str, *, timeout: float = 30.0, **options: Any) -> str:
        r = await self._http.post(
            f"{self._base}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": options},
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json().get("response", "")

    async def chat(self, payload: dict[str, Any]) -> httpx.Response:
        return await self._http.post(f"{self._base}/v1/chat/completions", json=payload, timeout=None)

    def stream_chat(self, payload: dict[str, Any]):
        return self._http.stream("POST", f"{self._base}/v1/chat/completions", json=payload, timeout=None)

    async def healthy(self) -> bool:
        try:
            r = await self._http.get(f"{self._base}/api/tags", timeout=5.0)
            return r.status_code == 200
        except httpx.HTTPError:
            return False
