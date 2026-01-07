from typing import Callable

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from app.repositories.users import UsersRepository
from app.services.user.service import UsersService
from app.storage.engine import async_session
from app.storage.models.user import Role


async def notify(role: Role, send: Callable, *args, **kwargs):
    try:
        async with async_session() as session:
            repo = UsersRepository(session)
            service = UsersService(repo)
            try:
                users = await service.get_users_by_role(role)
                for user in users:
                    await send(user.telegram_id, *args, **kwargs)
            except TelegramForbiddenError:
                pass
            except Exception as e:
                print(f"Failed to notify {role}: {e}")

    except TelegramBadRequest:
        pass
