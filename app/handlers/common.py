from aiogram import Router
from aiogram.types import CallbackQuery

from app.dialogs.rows.common import CloseCallback

router = Router()


@router.callback_query(CloseCallback.filter())
async def cb_close_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
