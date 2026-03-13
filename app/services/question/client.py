import asyncio
from typing import Any

import requests

from app.core.requests import EmbeddingRequestTemplate, request_templates


class EmbeddingClient:
    def __init__(
        self,
        template: EmbeddingRequestTemplate | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.template = template or request_templates.embedding
        self.timeout = timeout

    async def compute(self, text: str) -> list[float]:
        request_data = self.template.build(text)
        response_data = await asyncio.to_thread(self._send_request, request_data)
        embedding = self.template.extract(response_data)
        return [float(value) for value in embedding]

    def _send_request(self, request_data: dict[str, Any]) -> dict[str, Any]:
        response = requests.request(
            method=request_data["method"],
            url=request_data["url"],
            headers=request_data["headers"],
            json=request_data["body"],
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError("Embedding response must be a JSON object")
        return data


embedding_client = EmbeddingClient()
