
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request, HTTPException

from bot.handlers import (
    start_router,
    levels_router,
    categories_router,
)

app = FastAPI(title="Japanese SHIFU")

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(levels_router)
dp.include_router(categories_router)


@app.get("/")
async def home():
    return {"status": "Japanese SHIFU is running"}


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise HTTPException(
            status_code=500,
            detail="BOT_TOKEN environment variable is missing",
        )

    try:
        payload = await request.json()
        update = Update.model_validate(payload)

        async with Bot(token=token) as bot:
            await dp.feed_update(bot, update)

        return {"ok": True}

    except HTTPException:
        raise
    except Exception:
        # Token yoki ichki xatolarni javobga chiqarmaymiz.
        raise HTTPException(
            status_code=500,
            detail="Webhook processing failed",
        )
