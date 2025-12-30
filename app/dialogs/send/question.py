from typing import Awaitable, Callable

import app.dialogs.markups.question as mu
from app.core.constants.emoji import EmojiAction, EmojiStatus
from app.dialogs.actions import action_wrapper
from app.utils.format.output import format_id, format_question_output


# Input
@action_wrapper
async def send_enter_question_id(
    send: Callable[..., Awaitable[None]],
):
    await send(
        text=f"{EmojiAction.ENTER} Enter the question id",
    )


@action_wrapper
async def send_enter_question_text(
    send: Callable[..., Awaitable[None]],
):
    await send(
        text=f"{EmojiAction.ENTER} Enter the question text",
    )


@action_wrapper
async def send_enter_answer_text(
    send: Callable[..., Awaitable[None]],
):
    await send(
        text=f"{EmojiAction.ENTER} Enter the answer text",
    )


# Creation
@action_wrapper
async def send_confirm_creation(
    send: Callable[..., Awaitable[None]],
    question_text: str,
    answer_text: str,
):
    await send(
        text=(
            f"{EmojiAction.SELECT} Confirm creation?\n"
            f"{format_question_output(
                    question_text=question_text,
                    answer_text=answer_text
                )}"
        ),
        parse_mode="HTML",
        reply_markup=mu.confirm_creation,
    )


@action_wrapper
async def send_successfully_created(
    send: Callable[..., Awaitable[None]],
    id: int,
    question_text: str,
    answer_text: str,
):
    await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} Question has been successfully created:\n"
            f"{format_question_output(id, question_text, answer_text)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_found_similar(
    send: Callable[..., Awaitable[None]],
    id: int,
    question_text: str,
):
    await send(
        text=(
            f"{EmojiStatus.WARNING} A similar question already exists:\n"
            f"{format_question_output(id, question_text)}\n"
            f"{EmojiAction.SELECT} Confirm creation?"
        ),
        parse_mode="HTML",
        reply_markup=mu.confirm_similar,
    )


# async def send_failed_creation( # TODO: USAGE
#     send: Callable[..., Awaitable[None]],
#     exception="Unexcepted error.",
# ):
#     await send(
#         text=format_exception_output(f"Failed to create the question: {exception}"),
#         reply_markup=mu.back,
#     )


# Finding
@action_wrapper
async def send_successfully_found(
    send: Callable[..., Awaitable[None]],
    id: int,
    question_text: str,
    answer_text: str,
):
    await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} The question has been successfully found:\n"
            f"{format_question_output(id, question_text, answer_text)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )


@action_wrapper
async def send_not_found(send: Callable[..., Awaitable[None]], id: int):
    await send(
        text=f"{EmojiStatus.FAILED} Question {format_id(id)} not found",
        parse_mode="HTML",
        reply_markup=mu.back,
    )


# Delition
@action_wrapper
async def send_confirm_deletion(
    send: Callable[..., Awaitable[None]], id: int, question_text: str, answer_text: str
):
    await send(
        text=(
            f"{EmojiAction.SELECT} Confirm deletion?\n"
            f"{format_question_output(id, question_text, answer_text)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.confirm_deletion,
    )


@action_wrapper
async def send_successfully_deleted(
    send: Callable[..., Awaitable[None]],
    id: int,
    question_text: str,
    answer_text: str,
):
    await send(
        text=(
            f"{EmojiStatus.SUCCESSFUL} Next question has been successfully deleted:\n"
            f"{format_question_output(id, question_text, answer_text)}"
        ),
        parse_mode="HTML",
        reply_markup=mu.back,
    )
