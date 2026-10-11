
import json

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import DATA_DIR
from bot.keyboards.inline import (
    CATEGORIES,
    LEVELS,
    lessons_keyboard,
    categories_keyboard,
    back_to_lessons_keyboard,
)

router = Router()


def load_lessons(level: str) -> dict:
    path = DATA_DIR / f"{level.lower()}.json"

    if not path.is_file():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


@router.callback_query(F.data.startswith("category:"))
async def choose_category(callback: CallbackQuery):
    _, level, category = callback.data.split(":", 2)

    if level not in LEVELS or category not in CATEGORIES:
        await callback.answer("Noto'g'ri tanlov.", show_alert=True)
        return

    data = load_lessons(level)
    lessons = data.get(category, [])

    if not lessons:
        await callback.message.edit_text(
            f"{CATEGORIES[category]}\n\n"
            f"JLPT {level} uchun bu bo'limda darslar hali yo'q.",
            reply_markup=categories_keyboard(level),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        f"{CATEGORIES[category]}\n\n"
        "Darsni tanlang:",
        reply_markup=lessons_keyboard(level, category, lessons),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lesson:"))
async def show_lesson(callback: CallbackQuery):
    _, level, category, index_text = callback.data.split(":", 3)

    if level not in LEVELS or category not in CATEGORIES:
        await callback.answer("Noto'g'ri tanlov.", show_alert=True)
        return

    data = load_lessons(level)
    lessons = data.get(category, [])

    try:
        index = int(index_text)
        lesson = lessons[index]
    except (ValueError, IndexError, TypeError):
        await callback.answer(
            "Dars topilmadi.",
            show_alert=True,
        )
        return

    title = str(lesson.get("title", "Dars"))
    content = str(lesson.get("content", "Dars mazmuni mavjud emas."))

    text = f"📚 {title}\n━━━━━━━━━━━━━━━━\n\n{content}"

    if len(text) > 4000:
        text = text[:3950] + "\n\n... Davomi keyin qo'shiladi."

    await callback.message.edit_text(
        text,
        reply_markup=back_to_lessons_keyboard(level, category),
    )
    await callback.answer()
