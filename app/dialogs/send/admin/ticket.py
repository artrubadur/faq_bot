from datetime import datetime
from typing import Awaitable, Callable

from aiogram.types import Message

import app.dialogs.markups.ticket as mu
from app.core.constants.emojis import EmojiAction, EmojiStatus
from app.dialogs.actions import with_message_action
from app.utils.format.output import format_exception, format_ticket


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


@with_message_action
async def send_failed_creation(
    send: Callable[..., Awaitable[Message]],
    exception="Unexcepted error.",
) -> Message:
    return await send(
        text=format_exception(f"Failed to create the ticket: {exception}"),
        reply_markup=mu.back,
    )