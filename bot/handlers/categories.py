import json
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline import back_to_categories_keyboard

router = Router()

def load_level_data(level: str) -> dict:
    """bot/data/ papkasidan json faylni yuklab olish"""
    file_path = f"bot/data/{level.lower()}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@router.callback_query(F.data.startswith("cat:"))
async def category_handler(callback: CallbackQuery):
    _, category, level = callback.data.split(":")  # misol: cat:goi:N5
    
    data = load_level_data(level)
    cat_data = data.get(category, None)

    category_names = {
        "goi": "📖 Goi (Lug'at)",
        "kanji": "🈁 Kanji (Iyerogliflar)",
        "bunpo": "📚 Bunpo (Grammatika)",
        "dokkai": "📑 Dokkai (O'qish)"
    }
    
    cat_title = category_names.get(category, category.upper())

    if cat_data:
        text = f"✨ **{level} - {cat_title}**\n\n{cat_data}"
    else:
        text = f"✨ **{level} - {cat_title}**\n\n⚠️ Hozircha bu bo'limda ma'lumotlar tayyorlanmoqda..."

    await callback.message.edit_text(
        text=text,
        reply_markup=back_to_categories_keyboard(level),
        parse_mode="Markdown"
    )
    await callback.answer()
