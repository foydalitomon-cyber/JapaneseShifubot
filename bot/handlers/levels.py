
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    LEVELS,
    categories_keyboard,
    levels_keyboard,
)

router = Router()


@router.callback_query(F.data == "back:levels")
async def back_to_levels(callback: CallbackQuery):
    await callback.message.edit_text(
        "🇯🇵 JLPT darajangizni tanlang:",
        reply_markup=levels_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("level:"))
async def choose_level(callback: CallbackQuery):
    level = callback.data.split(":", 1)[1]

    if level not in LEVELS:
        await callback.answer(
            "Noto'g'ri daraja.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        f"📚 JLPT {level}\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "O'rganmoqchi bo'lgan bo'limingizni tanlang:",
        reply_markup=categories_keyboard(level),
    )
    await callback.answer()
