from aiogram.types import InlineKeyboardMarkup

import app.dialogs.rows.base as rows
from app.core.constants.dirs import (
    SETTINGS,
    USERS,
    USERS_CREATE,
    USERS_DELETE,
    USERS_UPDATE,
)

main = InlineKeyboardMarkup(
    inline_keyboard=rows.crud_rows(USERS[1]) + rows.back_row(SETTINGS),
)

back = InlineKeyboardMarkup(inline_keyboard=rows.back_row(USERS[1]))

cancel = InlineKeyboardMarkup(inline_keyboard=rows.cancel_row(USERS[1]))

confirm_creation = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(USERS_CREATE[1], USERS[1])
)

confirm_deletion = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(USERS_DELETE[1], USERS[1])
)

confirm_update = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(USERS_UPDATE[1], USERS[1])
)

field_save_update = InlineKeyboardMarkup(
    inline_keyboard=rows.field_rows(
        USERS_UPDATE[1],
        USERS[1],
        [rows.FieldButton("Username", "username"), rows.FieldButton("Role", "role")],
    )
)
