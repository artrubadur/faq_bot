from enum import StrEnum


class EmojiMenu(StrEnum):
    SETTINGS = "⚙"
    USERS = "👤"
    QUESTIONS = "📚"


class EmojiNav(StrEnum):
    BACK = "◀️"
    CANCEL = "✖️"
    CANCEL_CHANGES = "🚫"
    REJECT = "❌"
    CLOSE = "✖️"
    RIGHT = "▶️"
    LEFT = "◀️"
    DOWN = "🔽"
    UP = "🔼"


class EmojiAction(StrEnum):
    CREATE = "➕"
    GET = "🔍"
    UPDATE = "🔧"
    DELETE = "🗑️"
    LIST = "🗂"
    SAVE = "💾"
    ENTER = "📝"
    SELECT = "⏩"
    EMPTY = "🧹"


class EmojiStatus(StrEnum):
    CONFIRM = "✅"
    SUCCESSFUL = "✅"
    FAILED = "❌"
    WARNING = "⚠"


class EmojiSymbol(StrEnum):
    CHANGE = "➡️"
    INDEX = "#️⃣"
    RATING = "🚀"
    QUESTION = "🔍"
    ANSWER = "💡"
    EMBEDDING = "🧬"
