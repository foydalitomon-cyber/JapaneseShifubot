import os
from fastapi import FastAPI, Request, Header, HTTPException
from aiogram import Bot, Dispatcher, types
from bot.config import BOT_TOKEN
from bot.handlers import start, levels, categories

app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(levels.router)
dp.include_router(categories.router)

# Soxta so'rovlardan koranish uchun maxfiy kalit (xohlagan murakkab matningiz)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_super_secret_key_123")

@app.post("/api/webhook")
async def webhook(request: Request, x_telegram_bot_api_secret_token: str = Header(None)):
    # Telegram yuborgan secret-tokenni tekshirish
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Ruxsat berilmadi")
        
    json_str = await request.json()
    update = types.Update(**json_str)
    await dp.feed_update(bot, update)
    return {"ok": True}