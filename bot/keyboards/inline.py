
from aiogram.utils.keyboard import InlineKeyboardBuilder

LEVELS = ["N5", "N4", "N3", "N2", "N1"]

CATEGORIES = {
    "vocab": "📘 Goi — So'zlar",
    "kanji": "🈶 Kanji",
    "grammar": "📗 Bunpo — Grammatika",
    "reading": "📖 Dokkai — O'qish",
}


def levels_keyboard():
    kb = InlineKeyboardBuilder()

    for level in LEVELS:
        kb.button(
            text=f"JLPT {level}",
            callback_data=f"level:{level}",
        )

    kb.adjust(2, 2, 1)
    return kb.as_markup()


def categories_keyboard(level: str):
    kb = InlineKeyboardBuilder()

    for key, title in CATEGORIES.items():
        kb.button(
            text=title,
            callback_data=f"category:{level}:{key}",
        )

    kb.button(text="⬅️ Darajalar", callback_data="back:levels")
    kb.adjust(2, 2, 1)

    return kb.as_markup()


def lessons_keyboard(level: str, category: str, lessons: list):
    kb = InlineKeyboardBuilder()

    for index, lesson in enumerate(lessons):
        kb.button(
            text=lesson["title"],
            callback_data=f"lesson:{level}:{category}:{index}",
        )

    kb.button(
        text="⬅️ Bo'limlar",
        callback_data=f"level:{level}",
    )

    kb.adjust(1)
    return kb.as_markup()


def back_to_lessons_keyboard(level: str, category: str):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="⬅️ Darslar",
        callback_data=f"category:{level}:{category}",
    )
    return kb.as_markup()
