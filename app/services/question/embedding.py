from .sdk_instance import sdk


class EmbeddingService:
    def __init__(self, new_sdk=None) -> None:
        self.sdk = new_sdk or sdk
        self.model = self.sdk.models.text_embeddings("query")

    async def compute(self, text: str) -> tuple[float, ...]:
        response = await self.model.run(text)
        return response.embedding


embedding_service = EmbeddingService()
