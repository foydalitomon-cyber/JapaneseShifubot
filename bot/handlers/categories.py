
import json

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import DATA_DIR
from bot.keyboards.inline import (
    CATEGORIES,
    LEVELS,
    back_to_lessons_keyboard,
    categories_keyboard,
    lessons_keyboard,
)
from bot.languages import LANGUAGES, text


router = Router()


# ============================================================
# LOAD LESSON DATA
# ============================================================

def load_lessons(level: str) -> dict:
    path = DATA_DIR / f"{level.lower()}.json"

    if not path.is_file():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


# ============================================================
# CHOOSE CATEGORY
# ============================================================

@router.callback_query(F.data.startswith("category:"))
async def choose_category(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    parts = callback.data.split(":")

    # New format: category:language:level:category
    if len(parts) != 4:
        await callback.answer(
            "Please send /start and choose a language.",
            show_alert=True,
        )
        return

    _, lang, level, category = parts

    if (
        lang not in LANGUAGES
        or level not in LEVELS
        or category not in CATEGORIES
    ):
        await callback.answer(
            "Invalid selection.",
            show_alert=True,
        )
        return

    data = load_lessons(level)
    lessons = data.get(category, [])

    if not lessons:
        await callback.message.edit_text(
            f"{text(lang, category)}\n\n"
            f"{text(lang, 'empty')} JLPT {level}.",
            reply_markup=categories_keyboard(lang, level),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        f"{text(lang, category)}\n\n{text(lang, 'lessons')}",
        reply_markup=lessons_keyboard(
            lang,
            level,
            category,
            lessons,
        ),
    )

    await callback.answer()


# ============================================================
# BACK TO CATEGORIES
# ============================================================

@router.callback_query(F.data.startswith("back:categories:"))
async def back_to_categories(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    parts = callback.data.split(":")

    if len(parts) != 4:
        await callback.answer()
        return

    _, _, lang, level = parts

    if lang not in LANGUAGES or level not in LEVELS:
        await callback.answer("Invalid selection.", show_alert=True)
        return

    await callback.message.edit_text(
        f"🇯🇵 JLPT {level}\n\n{text(lang, 'category')}",
        reply_markup=categories_keyboard(lang, level),
    )

    await callback.answer()


# ============================================================
# OPEN LESSON
# ============================================================

@router.callback_query(F.data.startswith("lesson:"))
async def show_lesson(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    parts = callback.data.split(":")

    if len(parts) != 5:
        await callback.answer("Lesson not found.", show_alert=True)
        return

    _, lang, level, category, index_text = parts

    if (
        lang not in LANGUAGES
        or level not in LEVELS
        or category not in CATEGORIES
    ):
        await callback.answer("Invalid selection.", show_alert=True)
        return

    lessons = load_lessons(level).get(category, [])

    try:
        index = int(index_text)
        lesson = lessons[index]
    except (ValueError, IndexError, TypeError):
        await callback.answer(
            text(lang, "not_found"),
            show_alert=True,
        )
        return

    title = str(lesson.get("title", text(lang, "lessons")))
    content = str(lesson.get("content", text(lang, "missing")))

    message_text = f"🇯🇵 {title}\n━━━━━━━━━━━━━━━━━━\n\n{content}"

    if len(message_text) > 4000:
        message_text = message_text[:3950] + "\n\n..."

    await callback.message.edit_text(
        message_text,
        reply_markup=back_to_lessons_keyboard(
            lang,
            level,
            category,
        ),
    )

    await callback.answer()
