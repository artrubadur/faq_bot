from datetime import datetime
from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup, Message

import app.dialogs.markups.ticket as mu
import app.dialogs.rows.common as brows
import app.dialogs.rows.question as qrows
from app.core.constants.emojis import EmojiAction, EmojiStatus
from app.dialogs.actions import with_message_action
from app.utils.format.output import format_id, format_ticket


# Input
@with_message_action
async def send_enter_id(
    send: Callable[..., Awaitable[Message]],
    cancel_dir: str,
    dir: str,
    found_ticket_id: int | None = None,
) -> Message:
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=qrows.id_row(dir, found_ticket_id)
        + brows.cancel_row(cancel_dir)
    )
    return await send(
        text=f"{EmojiAction.ENTER} Enter the ticket id", reply_markup=reply_markup
    )


# Creation
@with_message_action
async def send_confirm_creation(
    send: Callable[..., Awaitable[Message]],
    author_id: int,
    question_text: str,
) -> Message:
    return await send(
        text=(
            f"{EmojiAction.SELECT} Confirm creation?\n"
            f"{format_ticket(
                    question_text=question_text,
                    author_id=author_id
                )}"
        ),
        parse_mode="HTML",
        reply_markup=mu.confirm_creation,
    )


@with_message_action
async def send_successfully_created(
    send: Callable[..., Awaitable[Message]],
    id: int,
    author_id: int,
    question_text: str,
    created_at: datetime,
) -> Message:
    return await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} Ticket has been successfully created:\n"
            f"{format_ticket(
                    id=id,
                    author_id=author_id,
                    question_text=question_text,
                    created_at=created_at
                )}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


# Finding
@with_message_action
async def send_successfully_found(
    send: Callable[..., Awaitable[Message]],
    id: int | None = None,
    author_id: int | None = None,
    responder_id: int | None = None,
    question_text: str | None = None,
    answer_text: str | None = None,
    created_at: datetime | None = None,
    answered_at: datetime | None = None,
) -> Message:
    return await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} The question has been successfully found:\n"
            f"{format_ticket(
                id,
                author_id,
                responder_id,
                question_text,
                answer_text,
                created_at,
                answered_at
            )}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@with_message_action
async def send_not_found(send: Callable[..., Awaitable[Message]], id: int) -> Message:
    return await send(
        text=f"{EmojiStatus.FAILED} Ticket {format_id(id)} not found",
        parse_mode="HTML",
        reply_markup=mu.back,
    )
