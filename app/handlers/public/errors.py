import traceback

from aiogram import Router
from aiogram.types import ErrorEvent

from app.dialogs.actions import SendAction
from app.dialogs.send.common import send_unexcepted_error, send_unhandled_exception
from app.services.notification import notify
from app.storage.models.user import Role
from app.utils.format.output import format_message

router = Router()


@router.errors()
async def errors_handler(event: ErrorEvent):
    exception = event.exception
    update = event.update

    message = update.message

    if message is not None:
        await send_unexcepted_error(message, SendAction.ANSWER)

    message_str = None if message is None else format_message(message)
    tb_string = traceback.format_exc()
    print(
        f"Unhandled error: {exception}\nMessage:\n{message_str}\nTraceback:\n{tb_string}"
    )

    await notify(Role.ADMIN, send_unhandled_exception, exception)

    return True
