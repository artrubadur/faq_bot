from app.core.config import config
from app.core.exceptions import SimilarityError
from app.repositories import QuestionsRepository
from app.services.question.embedding import EmbeddingService, embedding_service
from app.storage.models import Question


class QuestionsService:
    def __init__(
        self,
        repository: QuestionsRepository,
        simillarest_distance: float | None = None,
        simillar_distance: float | None = None,
        new_embedding_service: EmbeddingService | None = None,
    ):
        self.repository = repository
        self.simillarest_distance = simillarest_distance or (
            1 - config.questions.simillarest_threshold
        )
        self.simillar_distance = simillar_distance or (
            1 - config.questions.simillar_threshold
        )
        self.embedding_service = new_embedding_service or embedding_service

    async def create_question(
        self, question_text: str, question_answer: str, check_similarity: bool
    ) -> Question:
        embedding = await self.embedding_service.compute(question_text)

        if check_similarity:
            row = await self.repository.get_similar(
                embedding=embedding, limit=1, max_distance=self.simillarest_distance
            )
            if len(row) > 0:
                similar, distance = row[0]
                similarity = 1 - distance
                raise SimilarityError(
                    "A similar question already exists", similar, similarity
                )

        return await self.repository.create(
            question_text,
            question_answer,
            embedding,
        )

    async def get_question(self, id: int) -> Question:
        return await self.repository.get_by_id(id)

    async def get_questions_amount(self) -> int:
        return await self.repository.get_amount()

    async def get_paginated_questions(
        self, page: int, page_size: int, order_by: str, ascending: bool
    ) -> list[Question]:
        offset = (page - 1) * page_size
        questions = await self.repository.get_slice(
            offset, page_size, order_by, ascending
        )
        return list(questions)

    async def delete_question(self, id: int) -> Question:
        return await self.repository.delete(id)

    async def _get_similar_questions(
        self,
        question_text: str,
        amount: int,
    ) -> tuple[list[Question], list[float]]:
        embedding = await self.embedding_service.compute(question_text)
        rows = await self.repository.get_similar(
            embedding=embedding,
            limit=amount,
            max_distance=self.simillar_distance,
        )

        questions: list[Question] = [row[0] for row in rows]
        similarities: list[float] = [1 - row[1] for row in rows]

        if similarities:
            sim1 = similarities[0]
            sim2 = similarities[1] if len(similarities) > 1 else 0.0
            threshold = config.questions.simillarest_threshold

            if (
                sim1 >= threshold - 1e-6
            ):  # Handle floating-point precision issues for threshold == 1
                if threshold == 1:
                    await self.repository.increment_ratings([questions[0]], [1.0])
                else:
                    norm = (sim1 - threshold) / (1 - threshold)
                    norm = max(0.0, min(norm, 1.0))

                    gap = (sim1 - sim2) * 10
                    gap = max(0.0, min(gap, 1.0))

                    gain = norm**2 * gap

                    if gain > 0:
                        await self.repository.increment_ratings([questions[0]], [gain])

        return questions, similarities

    async def _get_most_popular_questions(
        self, amount: int, exclude_questions: list[Question] = []
    ) -> list[Question]:
        exclude_ids = [q.id for q in exclude_questions]
        questions = await self.repository.get_most_popular(amount, exclude_ids)
        return list(questions)

    async def suggest_questions(
        self,
        question_text: str,
        max_simillar_amount: int,
        max_popular_amount: int,
        max_amount: int,
    ) -> tuple[list[Question], bool]:
        similar, similarities = await self._get_similar_questions(
            question_text, max_simillar_amount + 1
        )

        popular_amount = min(max_amount - len(similar), max_popular_amount)
        popular = await self._get_most_popular_questions(popular_amount, similar)
        suggestions = similar + popular
        is_confident = (
            len(similarities) != 0
            and similarities[0] >= config.questions.simillarest_threshold
        )

        return suggestions, is_confident

    async def update_question(
        self,
        id: int,
        question_text: str,
        answer_text: str,
        rating: float,
        recompute_embedding: bool,
    ) -> Question:
        update_fields: dict = {
            "question_text": question_text,
            "answer_text": answer_text,
            "rating": rating,
        }

        if recompute_embedding:
            update_fields["embedding"] = await self.embedding_service.compute(
                question_text
            )

        return await self.repository.update(id, **update_fields)
