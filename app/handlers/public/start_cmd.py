from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.dialogs.actions import SendAction
from app.dialogs.send.public.start import send_start
from app.repositories import QuestionsRepository
from app.repositories.users import UsersRepository
from app.services.question.service import QuestionsService
from app.services.user.service import UsersService
from app.storage.engine import async_session
from app.storage.models.user import Role

router = Router()


@router.message(CommandStart())
async def cmd_handler(message: Message):
    name = message.from_user.full_name

    async with async_session() as session:
        questions_repo = QuestionsRepository(session)
        questions_service = QuestionsService(questions_repo)
        try:
            questions = await questions_service.get_most_popular_questions(7)
            await send_start(message, SendAction.ANSWER, name, questions)
        except Exception:
            await send_start(message, SendAction.ANSWER, name)

        user = message.from_user
        users_repo = UsersRepository(session)
        users_service = UsersService(users_repo)
        await users_service.create_user(user.id, user.username, Role.USER)
