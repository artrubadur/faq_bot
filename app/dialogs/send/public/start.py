from typing import Awaitable, Callable

from aiogram.types import Message, ReplyKeyboardRemove

from app.core.constants.files import Image
from app.dialogs.actions import action_wrapper


@action_wrapper
async def send_start(
    send: Callable[..., Awaitable[Message]], full_name: str
) -> Message:
    return await send(
        document=Image.GREETING.value,
        caption=f"You started the bot, {full_name}!",
        reply_markup=ReplyKeyboardRemove(),
    )
