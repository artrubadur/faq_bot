from app.core.exceptions import APIError
from app.core.messages import messages
from app.services.question.client import EmbeddingClient, embedding_client


class EmbeddingService:
    def __init__(self, new_client: EmbeddingClient | None = None) -> None:
        self.client = new_client or embedding_client

    async def compute(self, text: str) -> tuple[float, ...]:
        try:
            return await self.client.compute(text)
        except Exception:
            raise APIError(messages.exceptions.question.embedding_failed)


embedding_service = EmbeddingService()
