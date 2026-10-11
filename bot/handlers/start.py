python
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import language_keyboard, levels_keyboard
from bot.languages import LANGUAGES, text


router = Router()


# ============================================================
# START COMMAND
# ============================================================

@router.message(CommandStart())
async def start_handler(message: Message):
    welcome_message = (
        "🇯🇵 Japanese SHIFU\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🌏 Welcome to Japanese SHIFU!\n\n"
        "Please select your language:\n"
        "Tilni tanlang / Выберите язык"
    )

    await message.answer(
        welcome_message,
        reply_markup=language_keyboard(),
    )


# ============================================================
# LANGUAGE SELECTION
# ============================================================

@router.callback_query(F.data.startswith("language:"))
async def choose_language(callback: CallbackQuery):
    if not callback.data or not callback.message:
        await callback.answer()
        return

    language_code = callback.data.split(":", 1)[1]

    if language_code not in LANGUAGES:
        await callback.answer(
            "Language not found.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        text(language_code, "level"),
        reply_markup=levels_keyboard(),
    )

    await callback.answer()
