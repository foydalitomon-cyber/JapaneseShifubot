import os

# Kod ichiga token yozilmaydi, u Server muhitidan (Environment variables) o'qib olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/api/webhook"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN xatosi: Server muhitida BOT_TOKEN topilmadi!")