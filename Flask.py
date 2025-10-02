from aiogram import Bot, Dispatcher, executor, types
from flask import Flask
import asyncio
import threading

API_TOKEN = "ТВОЙ_ТОКЕН"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Бот працює через webhook!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# Aiogram-хендлер
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привіт! Я живий на Render 🌍")

async def on_startup(dp):
    await bot.set_webhook("https://gdzbot-1.onrender.com/webhook")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    executor.start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",
        on_startup=on_startup,
        skip_updates=True,
        host="0.0.0.0",
        port=10000
    )
