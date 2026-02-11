from datetime import datetime

from app.repositories import TicketsRepository
from app.storage.models.ticket import Ticket


class TicketsService:
    def __init__(self, repository: TicketsRepository):
        self.repository = repository

    async def create_ticket(self, author_id: int, question_text: str) -> Ticket:
        return await self.repository.create(author_id, question_text)

    async def get_ticket(self, id: int) -> Ticket:
        return await self.repository.get_by_id(id)

    async def get_ticket_amount(self) -> int:
        return await self.repository.get_amount()

    async def get_paginated_tickets(
        self, page: int, page_size: int, order_by: str, ascending: bool
    ) -> list[Ticket]:
        offset = (page - 1) * page_size
        users = await self.repository.get_slice(offset, page_size, order_by, ascending)
        return list(users)

    async def delete_ticket(self, id: int) -> Ticket:
        return await self.repository.delete(id)

    async def update_ticket(
        self,
        id: int,
        author_id: int,
        responder_id: int,
        question_text: str,
        answer_text: str,
        created_at: datetime,
        answered_at: datetime,
    ) -> Ticket:
        return await self.repository.update(
            id,
            author_id=author_id,
            responder_id=responder_id,
            question_text=question_text,
            answer_text=answer_text,
            created_at=created_at,
            answered_at=answered_at,
        )
