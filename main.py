from aiogram import executor
from loader import dp
import database as db

# імпортуємо хендлери
import admin
import dz
import loader
import ban
import database

async def on_startup(_):
    print("✅ Бот запущений")
    db.init_db()


if __name__ == "__main__":
    db.init_db()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
