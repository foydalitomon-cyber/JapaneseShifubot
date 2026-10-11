import json
from pathlib import Path
from html import escape

from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline import back_to_categories_keyboard

router = Router()

# JSON fayllarining aniq manzili
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_level_data(level: str) -> dict:
    """Kerakli JLPT darajasining JSON ma'lumotlarini yuklaydi."""
    level = level.upper()

    if level not in {"N5", "N4", "N3", "N2", "N1"}:
        return {}

    file_path = DATA_DIR / f"{level.lower()}.json"

    if not file_path.is_file():
        print(f"JSON fayli topilmadi: {file_path}")
        return {}

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print(f"JSON ichidagi ma'lumot dict emas: {file_path}")
            return {}

        return data

    except (json.JSONDecodeError, OSError) as error:
        print(f"JSON o'qish xatosi: {error}")
        return {}


@router.callback_query(F.data.startswith("cat:"))
async def category_handler(callback: CallbackQuery):
    parts = (callback.data or "").split(":")

    if len(parts) != 3:
        await callback.answer("Noto'g'ri bo'lim.", show_alert=True)
        return

    _, category, level = parts
    level = level.upper()

    category_names = {
        "goi": "Goi (Lug'at)",
        "kanji": "Kanji (Iyerogliflar)",
        "bunpo": "Bunpo (Grammatika)",
        "dokkai": "Dokkai (O'qish)",
    }

    if category not in category_names:
        await callback.answer("Bunday bo'lim mavjud emas.", show_alert=True)
        return

    data = load_level_data(level)
    cat_data = data.get(category)

    title = category_names[category]

    if cat_data is None or cat_data == "":
        content = "Hozircha bu bo'limda ma'lumotlar tayyorlanmoqda..."
    elif isinstance(cat_data, (dict, list)):
        content = json.dumps(
            cat_data,
            ensure_ascii=False,
            indent=2
        )
    else:
        content = str(cat_data)

    # HTML maxsus belgilarini xavfsiz chiqarish
    text = (
        f"<b>{escape(level)} - {escape(title)}</b>\n\n"
        f"{escape(content)}"
    )

    # Telegram bitta xabarda 4096 belgigacha qabul qiladi.
    if len(text) > 4000:
        text = text[:3950] + "\n\nMa'lumot qisqartirildi. JSON faylini kichik bo'limlarga ajratish kerak."

    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=back_to_categories_keyboard(level),
            parse_mode="HTML",
        )
    except Exception as error:
        print(f"Telegram xabari yangilanmadi: {error}")
        await callback.answer(
            "Xabarni ko'rsatishda xato yuz berdi.",
            show_alert=True
        )
        return

    await callback.answer()
