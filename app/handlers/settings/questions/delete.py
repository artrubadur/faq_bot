# pyright: reportArgumentType=false
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import NoResultFound

from app.dialogs import SendAction
from app.dialogs.rows.base import ConfirmCallback
from app.dialogs.send.base import send_invalid
from app.dialogs.send.question import (
    send_confirm_deletion,
    send_enter_question_id,
    send_not_found,
    send_successfully_deleted,
)
from app.repositories.questions import QuestionsRepository
from app.services.question.process import process_id_msg
from app.services.question.service import QuestionsService
from app.storage.db.engine import async_session

router = Router()

PARENT_DIR = "settings.questions"
DIR = "settings.questions.delete"


class Deletion(StatesGroup):
    waiting_for_id = State()


@router.callback_query(F.data == DIR)
async def question_get_cb_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await send_enter_question_id(
        callback.message,
        action=SendAction.EDIT,
    )
    await state.set_state(Deletion.waiting_for_id)


@router.message(Deletion.waiting_for_id)
async def user_delete_msg_identity_handler(message: Message, state: FSMContext):
    try:
        input_id = await process_id_msg(message)
    except ValueError as e:
        await send_invalid(message, PARENT_DIR, str(e), action=SendAction.ANSWER)
        return

    await state.update_data(input_id=input_id)

    async with async_session() as session:
        repo = QuestionsRepository(session)
        service = QuestionsService(repo)
        try:
            question = await service.read_question(input_id)
            await send_confirm_deletion(
                message,
                question.id,
                question.question_text,
                question.answer_text,
                action=SendAction.ANSWER,
            )
        except NoResultFound:
            await send_not_found(message, input_id, action=SendAction.ANSWER)

    await state.set_state(None)


@router.callback_query(ConfirmCallback.filter(F.dir == DIR))
async def user_delete_cb_confirm_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    input_id: int = data.pop("input_id")

    async with async_session() as session:
        repo = QuestionsRepository(session)
        service = QuestionsService(repo)
        try:
            question = await service.delete_question(input_id)
            await send_successfully_deleted(
                callback.message,
                question.id,
                question.question_text,
                question.answer_text,
                action=SendAction.EDIT,
            )
        except NoResultFound:
            await send_not_found(callback.message, input_id, action=SendAction.EDIT)

    await state.set_state(None)
