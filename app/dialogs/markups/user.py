from aiogram.types import InlineKeyboardMarkup

import app.dialogs.rows.base as rows

DIR = "settings.users"


main = InlineKeyboardMarkup(
    inline_keyboard=rows.crud_rows(DIR) + rows.back_row("settings"),
)

back = InlineKeyboardMarkup(inline_keyboard=rows.back_row(DIR))

cancel = InlineKeyboardMarkup(inline_keyboard=rows.cancel_row(DIR))

confirm_creation = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(f"{DIR}.create", DIR)
)

confirm_deletion = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(f"{DIR}.delete", DIR)
)

confirm_update = InlineKeyboardMarkup(
    inline_keyboard=rows.confirm_row(f"{DIR}.update", DIR)
)

field_save_update = InlineKeyboardMarkup(
    inline_keyboard=rows.field_rows(f"{DIR}.update", DIR, ["username", "role"])
)
