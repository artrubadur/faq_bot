from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup, Message

import app.dialogs.rows.root as rows
from app.core.constants.emojis import EmojiAction
from app.dialogs.actions import with_message_action
from app.utils.format.output import format_exception


@with_message_action
async def send_confirm_goto(
    send: Callable[..., Awaitable[Message]], dir: str
) -> Message:
    reply_markup = InlineKeyboardMarkup(inline_keyboard=rows.go_row(dir))

    return await send(
        text=f"{EmojiAction.SELECT} Go to `{dir}`?",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


@with_message_action
async def send_invalid_path(
    send: Callable[..., Awaitable[Message]], exception: str | None = None
) -> Message:
    return await send(
        text=format_exception(f"Failed to go: {exception}"),
    )
