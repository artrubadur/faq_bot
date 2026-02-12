from aiogram.types import InlineKeyboardMarkup

import app.dialogs.rows.common as rows
from app.core.constants.dirs import (
    TICKETS,
)

main = InlineKeyboardMarkup(
    inline_keyboard=rows.crud_rows(TICKETS[1])
    + rows.list_row(TICKETS[1])
    + rows.back_row(TICKETS[0]),
)