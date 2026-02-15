from aiogram.types import InlineKeyboardMarkup

import app.dialogs.rows.common as rows
from app.core.constants.dirs import TICKETS, TICKETS_CREATE

main = InlineKeyboardMarkup(
    inline_keyboard=rows.crud_rows(TICKETS[1])
    + rows.list_row(TICKETS[1])
    + rows.back_row(TICKETS[0]),
)

back = InlineKeyboardMarkup(inline_keyboard=rows.back_row(TICKETS[1]))

cancel = InlineKeyboardMarkup(inline_keyboard=rows.cancel_row(TICKETS[1]))

confirm_creation = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(TICKETS_CREATE[1], TICKETS[1], "create")
)
