from enum import Enum
from functools import wraps
from typing import Awaitable, Callable, Concatenate, ParamSpec

from aiogram.types import Message


class SendAction(str, Enum):
    ANSWER = "answer"
    REPLY = "reply"
    REPLY_DOCUMENT = "reply_document"
    EDIT = "edit"


async def do_action(message: Message, action: SendAction, **kwargs) -> Message:
    match action:
        case SendAction.EDIT:
            return await message.edit_text(**kwargs)  # type: ignore

        case SendAction.REPLY:
            return await message.reply(**kwargs)

        case SendAction.REPLY_DOCUMENT:
            return await message.reply_document(**kwargs)

        case _:
            return await message.answer(**kwargs)


P = ParamSpec("P")


def action_wrapper(
    func: Callable[Concatenate[Callable, P], Awaitable[Message]],
) -> Callable[Concatenate[Message, SendAction, P], Awaitable[Message]]:
    @wraps(func)
    async def inner(message: Message, action: SendAction, *args, **kwargs):
        async def send(**data):
            return await do_action(message, action, **data)

        return await func(
            send,
            *args,
            **kwargs,
        )

    return inner
