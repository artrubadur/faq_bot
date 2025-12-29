from numpy.random import rand

from app.repositories import QuestionsRepository
from app.storage.db.models import Question


def embedding_computer(question_text: str):  # TODO:
    return rand(1024)


class QuestionsService:
    def __init__(self, repository: QuestionsRepository):
        self.repository = repository

    async def create_question(
        self, question_text: str, question_answer: str
    ) -> Question:
        embedding = embedding_computer(question_text)
        return await self.repository.create(
            question_text,
            question_answer,
            embedding,
        )

    async def read_question(self, id: int) -> Question:
        return await self.repository.read(id)

    async def delete_question(self, id: int) -> Question:
        return await self.repository.delete(id)

    async def update_question(
        self,
        id: int,
        question_text: str | None,
        question_answer: str | None,
        recompute_embedding: bool,
    ) -> Question:
        update_fields = {}

        if question_text is not None:
            update_fields["question_text"] = question_text

            if recompute_embedding:
                update_fields["embedding"] = embedding_computer(question_text)
        else:
            if recompute_embedding:
                raise ValueError("Cannot recompute embedding without question_text.")

        if question_answer is not None:
            update_fields["question_text"] = question_answer

        return await self.repository.update(id, **update_fields)
