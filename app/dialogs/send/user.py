from typing import Awaitable, Callable

from aiogram.types import InlineKeyboardMarkup

import app.dialogs.markups.user as mu
import app.dialogs.rows.base as rows
import app.dialogs.rows.user as urows
from app.core.constants.emoji import EmojiAction, EmojiStatus
from app.dialogs.actions import action_wrapper
from app.utils.format.output import (
    format_edited_user_output,
    format_exception_output,
    format_user_output,
)


# Input
@action_wrapper
async def send_enter_identity(
    send: Callable[..., Awaitable[None]],
    dir: str,
    found_id: int | None = None,
    found_username: str | None = None,
    sender_id: int | None = None,
    sender_username: str | None = None,
):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=urows.identity_rows(
            dir, found_id, found_username, sender_id, sender_username
        )
    )
    await send(
        text=f"{EmojiAction.ENTER} Enter a telegram id, share contact or forward a message",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_enter_username(
    send: Callable[..., Awaitable[None]],
    dir: str,
    found_username: str | None = None,
    sender_username: str | None = None,
):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=urows.username_rows(dir, found_username, sender_username)
    )
    await send(
        text=f"{EmojiAction.ENTER} Enter a username",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_select_role(send: Callable[..., Awaitable[None]], dir: str):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=urows.role_rows(dir))
    await send(
        text=f"{EmojiAction.SELECT} Select a role:",
        reply_markup=reply_markup,
    )


# Creation
@action_wrapper
async def send_confirm_creation(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiAction.SELECT} Confirm creation?\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.confirm_creation,
    )


@action_wrapper
async def send_successfully_created(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiStatus.SUCCESSFUL} User has been successfully created:\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_failed_creation(
    send: Callable[..., Awaitable[None]],
    exception="Unexcepted error.",
):
    await send(
        text=format_exception_output(f"Failed to create the user: {exception}"),
        reply_markup=mu.back,
    )


# Finding
@action_wrapper
async def send_successfully_found(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} The user has been successfully found in the database:\n"
            f"{format_user_output(id=id, username=username, role=role)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_partially_found(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None = None,
    role: str | None = None,
):
    await send(
        text=(
            f"{EmojiStatus.WARNING} The user has been partially found but missing in the database:\n"
            f"{format_user_output(id=id, username=username, role=role)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_not_found(
    send: Callable[..., Awaitable[None]], id: int, username: str | None = None
):
    await send(
        text=f"{EmojiStatus.FAILED} User {username or id}` not found",
        parse_mode="Markdown",
        reply_markup=mu.back,
    )


# Deletion
@action_wrapper
async def send_confirm_deletion(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiAction.SELECT} Confirm deletion?\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.confirm_deletion,
    )


@action_wrapper
async def send_successfully_deleted(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiStatus.SUCCESSFUL} Next user has been successfully deleted:\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.back,
    )


# Update
@action_wrapper
async def send_confirm_update(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiAction.SELECT} Update this user?\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.confirm_update,
    )


@action_wrapper
async def send_changes(
    send: Callable[..., Awaitable[None]],
    id: int,
    edited_id: int,
    username: str | None,
    edited_username: str | None,
    role: str,
    edited_role: str,
):
    changes_text = format_edited_user_output(
        id, edited_id, username, edited_username, role, edited_role
    )
    await send(
        text=f"{changes_text}\n{EmojiAction.SELECT} Select field to edit:",
        parse_mode="HTML",
        reply_markup=mu.field_save_update,
    )


@action_wrapper
async def send_edit_username(
    send: Callable[..., Awaitable[None]],
    dir: str,
    found_username: str | None = None,
):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=urows.username_rows(dir, found_username, clear=True)
        + rows.cancel_row("settings.users.update")
    )

    await send(
        text=f"{EmojiAction.ENTER} Enter a username",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_edit_role(
    send: Callable[..., Awaitable[None]],
    dir: str,
):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=urows.role_rows(dir) + rows.cancel_row("settings.users.update")
    )

    await send(
        text=f"{EmojiAction.ENTER} Select a role:",
        reply_markup=reply_markup,
    )


@action_wrapper
async def send_successfully_updated(
    send: Callable[..., Awaitable[None]],
    id: int,
    username: str | None,
    role: str,
):
    await send(
        text=f"{EmojiStatus.SUCCESSFUL} User has been successfully updated:\n{format_user_output(id=id, username=username, role=role)}",
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_failed_update(
    send: Callable[..., Awaitable[None]],
    exception="Unexcepted error.",
):
    await send(
        text=format_exception_output(f"Failed to update the user: {exception}"),
        reply_markup=mu.back,
    )
