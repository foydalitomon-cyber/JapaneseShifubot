from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Bosh menyu: N5 - N1 darajalar tugmalari"""
    buttons = [
        [InlineKeyboardButton(text="🔴 N5 (Boshlang'ich)", callback_data="level:N5")],
        [
            InlineKeyboardButton(text="🟠 N4", callback_data="level:N4"),
            InlineKeyboardButton(text="🟡 N3", callback_data="level:N3")
        ],
        [
            InlineKeyboardButton(text="🟢 N2", callback_data="level:N2"),
            InlineKeyboardButton(text="🔵 N1 (Yuqori)", callback_data="level:N1")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def categories_keyboard(level: str) -> InlineKeyboardMarkup:
    """Tanlangan daraja ichidagi Goi, Kanji, Bunpo, Dokkai bo'limlari"""
    buttons = [
        [
            InlineKeyboardButton(text="📖 Goi (語彙)", callback_data=f"cat:goi:{level}"),
            InlineKeyboardButton(text="🈁 Kanji (漢字)", callback_data=f"cat:kanji:{level}")
        ],
        [
            InlineKeyboardButton(text="📚 Bunpo (文法)", callback_data=f"cat:bunpo:{level}"),
            InlineKeyboardButton(text="📑 Dokkai (読解)", callback_data=f"cat:dokkai:{level}")
        ],
        [InlineKeyboardButton(text="⬅️ Bosh menyuga qaytish", callback_data="back_to_levels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_categories_keyboard(level: str) -> InlineKeyboardMarkup:
    """Bo'lim ichidan daraja menyusiga qaytish tugmasi"""
    buttons = [
        [InlineKeyboardButton(text=f"⬅️ {level} bo'limlariga qaytish", callback_data=f"level:{level}")],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_levels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
