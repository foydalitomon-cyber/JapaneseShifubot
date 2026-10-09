from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"Konnichiwa, {message.from_user.first_name}! ⛩\n\n"
        "**Japanese SHIFU** botiga xush kelibsiz!\n"
        "Yapon tilini o'rganish uchun o'zingizga kerakli **JLPT darajasini** tanlang:"
    )
    await message.answer(text=welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "back_to_levels")
async def back_to_levels_handler(callback: CallbackQuery):
    text = "Kerakli **JLPT darajasini** tanlang:"
    await callback.message.edit_text(text=text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")
    await callback.answer()
