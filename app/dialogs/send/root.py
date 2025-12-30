from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove

import app.dialogs.rows.root as rows
from app.core.constants.emoji import EmojiAction
from app.core.constants.files import Images
from app.dialogs.actions import action_wrapper
from app.utils.format.output import format_exception_output


@action_wrapper
async def send_start(send: Callable[..., Awaitable[None]], full_name: str):
    await send(
        document=Images.GREETING.value,
        caption=f"You started the bot, {full_name}!",
        reply_markup=ReplyKeyboardRemove(),
    )


@action_wrapper
async def send_confirm_goto(send: Callable[..., Awaitable[None]], dir: str):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=rows.go_row(dir))

    await send(
        text=f"{EmojiAction.SELECT} Go to `{dir}`?",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_invalid_path(
    send: Callable[..., Awaitable[None]], exception: str | None = None
):
    await send(
        text=format_exception_output(f"Failed to go: {exception}"),
    )
