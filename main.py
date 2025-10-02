import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from loader import dp, bot
import database as db
import admin
import dz
import ban

# 🔹 Налаштування
WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"  # слухати всі інтерфейси
WEBAPP_PORT = int(os.getenv("PORT", 5000))  # Render задає PORT

async def on_startup(dp):
    print("✅ Бот запущений на Render (webhook)")
    db.init_db()
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    print("🛑 Бот зупинений")
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
