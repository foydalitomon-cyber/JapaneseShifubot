
import asyncio

from aiogram import Bot, Dispatcher

from bot.config import get_bot_token
from bot.handlers import (
    start_router,
    levels_router,
    categories_router,
)


async def main():
    bot = Bot(token=get_bot_token())
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(levels_router)
    dp.include_router(categories_router)

    try:
        # Polling rejimi webhookni o'chiradi.
        await bot.delete_webhook(drop_pending_updates=True)

        print("Japanese SHIFU ishga tushdi!", flush=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
