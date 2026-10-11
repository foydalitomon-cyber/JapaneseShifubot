
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import levels_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🇯🇵 Japanese SHIFU\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "Yapon tilini bosqichma-bosqich o'rganing.\n\n"
        "JLPT darajangizni tanlang:",
        reply_markup=levels_keyboard(),
    )
