from __future__ import annotations

import httpx


class ModelClientError(RuntimeError):
    pass


class LocalModelClient:
    def __init__(
        self,
        endpoint: str,
        model_name: str,
        *,
        timeout_seconds: float = 300.0,
        max_tokens: int = 512,
    ) -> None:
        self.endpoint = endpoint
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens

    async def chat(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(self.endpoint, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ModelClientError(f"Local model endpoint failed: {exc}") from exc

        data = response.json()
        try:
            return str(data["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelClientError("Local model endpoint returned an unexpected response shape.") from exc


class MockModelClient:
    async def chat(self, messages: list[dict[str, str]]) -> str:
        user = next((message["content"] for message in reversed(messages) if message["role"] == "user"), "")
        return (
            "Mock local model response. The app and RAG wiring are working. "
            f"Last user request: {user[:300]}"
        )
