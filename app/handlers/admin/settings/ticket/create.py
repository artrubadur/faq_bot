from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError

from app.core.constants.dirs import TICKETS_CREATE
from app.dialogs.actions import SendAction
from app.dialogs.rows.common import ConfirmCallback
from app.dialogs.rows.user import IdentityCallback
from app.dialogs.send.admin.question import send_enter_question_text
from app.dialogs.send.admin.ticket import (
    send_confirm_creation,
    send_successfully_created,
    send_failed_creation
)
from app.dialogs.send.admin.user import send_enter_identity
from app.dialogs.send.common import send_invalid
from app.repositories.tickets import TicketsRepository
from app.services.question.process import process_question_text_msg
from app.services.ticket.service import TicketsService
from app.services.user.process import process_identity_msg
from app.storage.core import async_session
from app.utils.history.last_message import LastMessage

router = Router()

PARENT_DIR, DIR = TICKETS_CREATE


class Creation(StatesGroup):
    waiting_for_identity = State()
    waiting_for_question_text = State()


@router.callback_query(F.data == DIR)
async def ticket_create_cb_handler(
    callback: CallbackQuery, last_message: LastMessage, state: FSMContext
):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    found_user_id: int | None = data.get("glb_found_user_id", None)
    found_username = data.get("glb_found_username", None)

    sent_message = await send_enter_identity(
        callback.message,  # pyright: ignore[reportArgumentType]
        SendAction.EDIT,
        PARENT_DIR,
        DIR,
        found_user_id,
        found_username,
    )
    await last_message.set(sent_message, state)

    await state.set_state(Creation.waiting_for_identity)


async def process_identity_handler(
    message: Message,
    last_message: LastMessage,
    state: FSMContext,
    input_id: int,
    *,
    send_action: SendAction,
):
    await state.update_data(tmp_input_id=input_id)

    sent_message = await send_enter_question_text(message, send_action, PARENT_DIR)
    await last_message.set(sent_message, state)

    await state.set_state(Creation.waiting_for_question_text)


@router.message(Creation.waiting_for_identity)
async def ticket_create_msg_identity_handler(
    message: Message, last_message: LastMessage, state: FSMContext
):
    await last_message.edit_reply_markup(message, state)

    try:
        input_id, _ = await process_identity_msg(message)
    except ValueError as e:
        sent_message = await send_invalid(
            message, SendAction.ANSWER, PARENT_DIR, str(e)
        )
        await last_message.set(sent_message, state)
        return

    await process_identity_handler(
        message,
        last_message,
        state,
        input_id,
        send_action=SendAction.ANSWER,
    )


@router.callback_query(IdentityCallback.filter(F.dir == DIR))
async def ticket_create_cb_identity_handler(
    callback: CallbackQuery,
    last_message: LastMessage,
    callback_data: IdentityCallback,
    state: FSMContext,
):
    await callback.answer("")
    await callback.message.edit_reply_markup(reply_markup=None)

    input_id = callback_data.id

    await process_identity_handler(
        callback.message,  # pyright: ignore[reportArgumentType]
        last_message,
        state,
        input_id,
        send_action=SendAction.EDIT,
    )


@router.message(Creation.waiting_for_question_text)
async def ticket_create_msg_question_text_handler(
    message: Message, last_message: LastMessage, state: FSMContext
):
    await last_message.edit_reply_markup(message, state)

    try:
        input_question_text = await process_question_text_msg(message)
    except ValueError as e:
        sent_message = await send_invalid(
            message, SendAction.ANSWER, PARENT_DIR, str(e)
        )
        await last_message.set(sent_message, state)
        return

    await state.update_data(tmp_input_question_text=input_question_text)

    data = await state.get_data()
    input_id: int = data["tmp_input_id"]

    sent_message = await send_confirm_creation(
        message, SendAction.ANSWER, input_id, input_question_text
    )
    await last_message.set(sent_message, state)

    await state.set_state(None)


@router.callback_query(ConfirmCallback.filter(F.dir == DIR and F.step == "create"))
async def ticket_create_cb_create_confirm_handler(
    callback: CallbackQuery, state: FSMContext
):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    input_id: int = data.pop("tmp_input_id")
    input_question_text: str = data.pop("tmp_input_question_text")

    async with async_session() as session:
        repo = TicketsRepository(session)
        service = TicketsService(repo)
        try:
            ticket = await service.create_ticket(input_id, input_question_text)
            await state.set_data(data)
            await send_successfully_created(
                callback.message,  # pyright: ignore[reportArgumentType]
                SendAction.EDIT,
                ticket.id,
                ticket.author_id,
                ticket.question_text,
                ticket.created_at,
            )
        except IntegrityError:
            await send_failed_creation(
                callback.message,  # pyright: ignore[reportArgumentType]
                SendAction.EDIT,
                "Author is missing in the database",
            )
