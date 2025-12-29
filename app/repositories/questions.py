from numpy import ndarray
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.storage.db.models import Question


class QuestionsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, question_text: str, answer_text: str, embedding: ndarray
    ) -> Question:
        new_question = Question(
            question_text=question_text, answer_text=answer_text, embedding=embedding
        )
        self.session.add(new_question)
        await self.session.commit()
        await self.session.refresh(new_question)
        return new_question

    async def read(self, id: int) -> Question:
        question = await self.session.execute(select(Question).where(Question.id == id))
        return question.scalar_one()

    async def update(self, id: int, **kwargs) -> Question:
        question = await self.read(id)
        for key, value in kwargs.items():
            setattr(question, key, value)
        await self.session.commit()
        return question

    async def delete(self, id: int):
        question = await self.read(id)
        await self.session.delete(question)
        await self.session.commit()
        return question
