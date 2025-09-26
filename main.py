from aiogram import Bot, Dispatcher, executor, types
from flask import Flask
from threading import Thread

# 🔑 Встав сюди свій токен від BotFather
API_TOKEN = "8065465326:AAEV8aYGEEgDyWZwPZikBJIwl7LkB99TU5I"

# список айді адмінів (тільки вони можуть міняти дз)
ADMINS = [7618560125]  # заміни на свій Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# тут зберігається домашнє завдання
homework_text = "Домашнє завдання ще не встановлено ❌"


# ---------------------------
# Команди бота
# ---------------------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📚 Домашнє завдання")
    await message.answer("Привіт! 👋\nЩо тобі треба?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "📚 Домашнє завдання")
async def show_homework(message: types.Message):
    await message.answer(f"📌 Домашнє завдання:\n\n{homework_text}")


@dp.message_handler(commands=["setdz"])
async def set_homework(message: types.Message):
    global homework_text
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args:
            homework_text = args
            await message.answer("✅ Домашнє завдання оновлено!")
        else:
            await message.answer("⚠️ Напиши так: /setdz Текст_завдання")
    else:
        await message.answer("⛔ У тебе нема прав міняти ДЗ!")


# ---------------------------
# Веб-сервер (щоб Replit не засинав)
# ---------------------------
app = Flask('')

@app.route('/')
def home():
    return "Я живий!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# ---------------------------
# Запуск бота
# ---------------------------
if __name__ == "__main__":
    keep_alive()   # запускаємо веб-сервер
    executor.start_polling(dp, skip_updates=True)  # запускаємо бота
