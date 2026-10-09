import sys
import os

# ルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from bot.config import BOT_TOKEN
from bot.handlers import start, levels, categories

app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(levels.router)
dp.include_router(categories.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Japanese SHIFU Bot is running!"}

@app.post("/api/webhook")
async def webhook(request: Request):
    json_str = await request.json()
    update = types.Update(**json_str)
    await dp.feed_update(bot, update)
    return {"ok": True}