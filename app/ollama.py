from typing import Any

import httpx


class OllamaClient:
    """Async wrapper over the Ollama HTTP API, backed by a shared httpx client."""

    def __init__(self, base_url: str, http: httpx.AsyncClient) -> None:
        self._base = base_url.rstrip("/")
        self._http = http

    async def generate(
        self,
        model: str,
        prompt: str,
        *,
        timeout: float = 30.0,
        **options: Any,
    ) -> str:
        response = await self._http.post(
            f"{self._base}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": options},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json().get("response", "")

    async def chat(self, payload: dict[str, Any]) -> httpx.Response:
        return await self._http.post(
            f"{self._base}/v1/chat/completions", json=payload, timeout=None
        )

    def stream_chat(self, payload: dict[str, Any]):
        return self._http.stream(
            "POST", f"{self._base}/v1/chat/completions", json=payload, timeout=None
        )

    async def healthy(self) -> bool:
        try:
            response = await self._http.get(f"{self._base}/api/tags", timeout=5.0)
            return response.status_code == 200
        except httpx.HTTPError:
            return False
