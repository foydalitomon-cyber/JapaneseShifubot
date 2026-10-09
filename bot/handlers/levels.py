from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline import categories_keyboard

router = Router()

@router.callback_query(F.data.startswith("level:"))
async def level_selected_handler(callback: CallbackQuery):
    level = callback.data.split(":")[1]  # N5, N4, N3, N2 yoki N1
    text = (
        f"🎯 **Siz {level} darajasini tanladingiz!**\n\n"
        "O'rganmoqchi bo'lgan bo'limingizni tanlang:"
    )
    await callback.message.edit_text(text=text, reply_markup=categories_keyboard(level), parse_mode="Markdown")
    await callback.answer()
