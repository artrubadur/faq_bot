from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup

import app.dialogs.rows.base as rows
from app.core.constants.emoji import EmojiStatus
from app.dialogs.actions import action_wrapper


@action_wrapper
async def send_invalid(
    send: Callable[..., Awaitable[None]], dir: str, text: str | None
):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=rows.back_row(dir))

    await send(
        text=f"{EmojiStatus.WARNING} {text}. Retry or back",
        reply_markup=reply_markup,
    )
