import os
from aiogram import executor
from aiogram.utils.executor import start_webhook
from loader import dp, bot
import database as db
import admin
import dz
import ban
import flask

# --- Render settings ---
WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))


async def on_startup(dp):
    print("✅ Бот стартував")
    db.init_db()
    # Встановлюємо webhook
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    print("🛑 Бот зупиняється")
    await bot.delete_webhook()


if __name__ == "__main__":
    if os.getenv("RENDER"):  # якщо запущено на Render
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:  # локально
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
