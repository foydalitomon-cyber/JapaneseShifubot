
from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    LEVELS,
    categories_keyboard,
    levels_keyboard,
)
from bot.languages import LANGUAGES, text


router = Router()


# ============================================================
# BACK TO LEVELS
# ============================================================

@router.callback_query(F.data.startswith("back:levels:"))
async def back_to_levels(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    lang = callback.data.split(":", 2)[2]

    if lang not in LANGUAGES:
        await callback.answer("Language not found.", show_alert=True)
        return

    await callback.message.edit_text(
        text(lang, "level"),
        reply_markup=levels_keyboard(lang),
    )

    await callback.answer()


# ============================================================
# CHOOSE JLPT LEVEL
# ============================================================

@router.callback_query(F.data.startswith("level:"))
async def choose_level(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    parts = callback.data.split(":")

    # New format: level:language:level
    if len(parts) == 3:
        _, lang, level = parts
    else:
        await callback.answer(
            "Please send /start and choose a language.",
            show_alert=True,
        )
        return

    if lang not in LANGUAGES or level not in LEVELS:
        await callback.answer(
            text(lang, "invalid") if lang in LANGUAGES else "Invalid selection.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        f"🇯🇵 JLPT {level}\n\n{text(lang, 'category')}",
        reply_markup=categories_keyboard(lang, level),
    )

    await callback.answer()
