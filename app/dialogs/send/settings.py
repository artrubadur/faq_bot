from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup

import app.dialogs.markups.question as qmu
import app.dialogs.markups.user as umu
import app.dialogs.rows.base as rows
import app.dialogs.rows.settings as srows
from app.core.constants.emoji import EmojiMenu
from app.dialogs.actions import action_wrapper


@action_wrapper
async def send_settings_menu(send: Callable[..., Awaitable[None]]):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=srows.section_rows() + rows.close_row()
    )

    await send(
        text=f"{EmojiMenu.SETTINGS} Settings",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_users_menu(
    send: Callable[..., Awaitable[None]],
):
    await send(
        text=f"{EmojiMenu.USERS} User Management",
        reply_markup=umu.main,
    )


@action_wrapper
async def send_questions_menu(
    send: Callable[..., Awaitable[None]],
):
    await send(
        text=f"{EmojiMenu.QUESTIONS} Question Management",
        reply_markup=qmu.main,
    )
