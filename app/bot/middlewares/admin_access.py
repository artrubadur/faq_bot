from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import SkipHandler
from loguru import logger
from sqlalchemy.exc import NoResultFound

from app.bot.storage import LSTContext
from app.repositories import UsersRepository
from app.services import UsersService
from app.storage.core import async_session
from app.storage.models.user import Role


class AdminAccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: LSTContext | None = data.get("state")
        from_user = getattr(event, "from_user", None)

        if state is None or from_user is None:
            raise SkipHandler()

        sender_id: int = from_user.id
        sender_role = await self._resolve_sender_role(sender_id, state)
        data["sender_role"] = sender_role

        if sender_role != Role.ADMIN:
            logger.info(
                "Admin handler skipped: sender is not admin",
                tg_id=sender_id,
                role=sender_role,
            )
            raise SkipHandler()

        return await handler(event, data)

    async def _resolve_sender_role(self, sender_id: int, state: LSTContext) -> str:
        cached_role: str | None = await state.storage.get_value(
            state.key, "sender_role", None, "long"
        )
        if cached_role:
            return cached_role

        sender_role = await self._get_role_from_db(sender_id)
        await state.storage.update_data(state.key, {"sender_role": sender_role}, "long")
        return sender_role

    async def _get_role_from_db(self, sender_id: int) -> str:
        try:
            async with async_session() as session:
                repo = UsersRepository(session)
                service = UsersService(repo)
                user = await service.get_user(sender_id)
                return user.role
        except NoResultFound:
            return Role.USER
