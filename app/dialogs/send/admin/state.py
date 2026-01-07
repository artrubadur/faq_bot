from json import dumps
from typing import Any, Awaitable, Callable

from aiogram.types import Message

from app.dialogs.actions import with_message_action


@with_message_action
async def send_state(
    send: Callable[..., Awaitable[Message]], data: dict[str, Any]
) -> Message:
    str_data = dumps(data, indent=2)

    return await send(
        text=f"Stored data:\n{str_data}",
    )
