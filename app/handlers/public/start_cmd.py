from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.dialogs.actions import SendAction
from app.dialogs.send.public.start import send_start
from app.repositories import QuestionsRepository
from app.services.question.service import QuestionsService
from app.storage.engine import async_session

router = Router()


@router.message(CommandStart())
async def cmd_handler(message: Message):
    name = message.from_user.full_name

    async with async_session() as session:
        repo = QuestionsRepository(session)
        service = QuestionsService(repo)
        try:
            questions = await service.get_most_popular_questions(7)
            await send_start(message, SendAction.ANSWER, name, questions)
        except Exception:
            await send_start(message, SendAction.ANSWER, name)
