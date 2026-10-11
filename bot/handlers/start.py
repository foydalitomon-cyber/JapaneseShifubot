
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import language_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🇯🇵 Japanese SHIFU\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "🌏 Welcome to Japanese SHIFU!\n\n"
        "Please select your language:\n"
        "Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard(),
    )
