from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup, Message

import app.dialogs.rows.root as rows
from app.core.constants.emojis import EmojiAction
from app.dialogs.actions import action_wrapper
from app.utils.format.output import format_exception


@action_wrapper
async def send_confirm_goto(
    send: Callable[..., Awaitable[Message]], dir: str
) -> Message:
    reply_markup = InlineKeyboardMarkup(inline_keyboard=rows.go_row(dir))

    return await send(
        text=f"{EmojiAction.SELECT} Go to `{dir}`?",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_invalid_path(
    send: Callable[..., Awaitable[Message]], exception: str | None = None
) -> Message:
    return await send(
        text=format_exception(f"Failed to go: {exception}"),
    )
