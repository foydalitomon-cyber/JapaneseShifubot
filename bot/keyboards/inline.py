
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.languages import LANGUAGES, text


LANGUAGE_NAMES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O‘zbekcha",
    "hi": "🇮🇳 हिन्दी",
    "ar": "🇸🇦 العربية",
    "id": "🇮🇩 Indonesia",
    "my": "🇲🇲 မြန်မာ",
    "ja": "🇯🇵 日本語",
    "zh": "🇨🇳 中文",
}

LEVELS = ["N5", "N4", "N3", "N2", "N1"]

CATEGORIES = ["vocab", "kanji", "grammar", "reading"]


def language_keyboard():
    kb = InlineKeyboardBuilder()

    for code, name in LANGUAGE_NAMES.items():
        kb.button(
            text=name,
            callback_data=f"language:{code}",
        )

    kb.adjust(3, 3, 3)
    return kb.as_markup()


def levels_keyboard(lang: str):
    kb = InlineKeyboardBuilder()

    for level in LEVELS:
        kb.button(
            text=f"JLPT {level}",
            callback_data=f"level:{lang}:{level}",
        )

    kb.adjust(2, 2, 1)
    return kb.as_markup()


def categories_keyboard(lang: str, level: str):
    kb = InlineKeyboardBuilder()

    for category in CATEGORIES:
        kb.button(
            text=text(lang, category),
            callback_data=f"category:{lang}:{level}:{category}",
        )

    kb.button(
        text=text(lang, "back_levels"),
        callback_data=f"back:levels:{lang}",
    )

    kb.adjust(2, 2, 1)
    return kb.as_markup()


def lessons_keyboard(
    lang: str,
    level: str,
    category: str,
    lessons: list,
):
    kb = InlineKeyboardBuilder()

    for index, lesson in enumerate(lessons):
        kb.button(
            text=str(lesson.get("title", f"Lesson {index + 1}")),
            callback_data=f"lesson:{lang}:{level}:{category}:{index}",
        )

    kb.button(
        text=text(lang, "back_categories"),
        callback_data=f"back:categories:{lang}:{level}",
    )

    kb.adjust(1)
    return kb.as_markup()


def back_to_lessons_keyboard(
    lang: str,
    level: str,
    category: str,
):
    kb = InlineKeyboardBuilder()

    kb.button(
        text=text(lang, "back_lessons"),
        callback_data=f"category:{lang}:{level}:{category}",
    )

    return kb.as_markup()
