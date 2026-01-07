from typing import Awaitable, Callable

from aiogram.types import Message

from app.dialogs.actions import with_message_action
from app.storage.models.question import Question


@with_message_action
async def send_similar(
    send: Callable[..., Awaitable[Message]], questions: list[tuple[Question, float]]
) -> Message:
    most_similar = questions[0][0]
    return await send(text=most_similar.answer_text)


@with_message_action
async def send_invalid(
    send: Callable[..., Awaitable[Message]], exception: str
) -> Message:
    return await send(text=f"{exception}. Try to reformulate it and ask it again")
