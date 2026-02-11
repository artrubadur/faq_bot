from typing import Sequence, cast

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.models.ticket import Ticket


class TicketsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, author_id: int, question_text: str) -> Ticket:
        ticket = Ticket(author_id=author_id, question_text=question_text)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def get_by_id(self, id: int) -> Ticket:
        ticket = await self.session.execute(select(Ticket).where(Ticket.id == id))
        return ticket.scalar_one()

    async def get_slice(
        self, offset: int, limit: int, order_by: str, ascending: bool
    ) -> Sequence[Ticket]:
        col = getattr(Ticket, order_by)

        order_expr = col.asc() if ascending else col.desc()

        tickets = await self.session.execute(
            select(Ticket).order_by(order_expr).offset(offset).limit(limit)
        )
        return tickets.scalars().all()

    async def get_amount(self) -> int:
        amount = await self.session.execute(select(func.count()).select_from(Ticket))
        return cast(int, amount.scalar())

    async def update(self, id: int, **kwargs) -> Ticket:
        ticket = await self.get_by_id(id)
        for key, value in kwargs.items():
            setattr(ticket, key, value)
        await self.session.commit()
        return ticket

    async def delete(self, id: int):
        ticket = await self.get_by_id(id)
        await self.session.delete(ticket)
        await self.session.commit()
        return ticket
