import os
import json
from aiogram import Bot, Dispatcher, executor, types
from flask import Flask
from threading import Thread

# ---------------------------
# Токен (бери з Render -> Environment -> API_TOKEN)
# ---------------------------
API_TOKEN = os.getenv("API_TOKEN")  # <-- створи в Render env var з цим ім'ям

if not API_TOKEN:
    raise ValueError("❌ Немає токена! Додай API_TOKEN в Environment Variables")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ---------------------------
# Функції для роботи з JSON
# ---------------------------
def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------------------------
# Дані
# ---------------------------
ADMINS = load_json("admins.json", [7618560125, 6964713379])  # твої айдішки тут
BANNED = load_json("banned.json", [])
homework_text = load_json("homework.json", "Домашнє завдання ще не встановлено ❌")
news_text = load_json("news.json", "Новини ще не встановлені ❌")

# ---------------------------
# Команди бота
# ---------------------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id in BANNED:
        await message.answer("⛔ Ти забанений у цьому боті!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📚 Домашнє завдання", "📰 Новини")
    await message.answer("Привіт! 👋\nЩо тобі треба?", reply_markup=keyboard)

# Домашнє завдання
@dp.message_handler(lambda message: message.text == "📚 Домашнє завдання")
async def show_homework(message: types.Message):
    if message.from_user.id in BANNED:
        await message.answer("⛔ Ти забанений у цьому боті!")
        return
    await message.answer(f"📌 Домашнє завдання:\n\n{homework_text}")

# Новини
@dp.message_handler(lambda message: message.text == "📰 Новини")
async def show_news(message: types.Message):
    if message.from_user.id in BANNED:
        await message.answer("⛔ Ти забанений у цьому боті!")
        return
    await message.answer(f"📰 Новини:\n\n{news_text}")

# Встановити ДЗ
@dp.message_handler(commands=["setdz"])
async def set_homework(message: types.Message):
    global homework_text
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args:
            homework_text = args
            save_json("homework.json", homework_text)
            await message.answer("✅ Домашнє завдання оновлено!")
        else:
            await message.answer("⚠️ Напиши так: /setdz Текст_завдання")
    else:
        await message.answer("⛔ У тебе нема прав міняти ДЗ!")

# Встановити новини
@dp.message_handler(commands=["setnews"])
async def set_news(message: types.Message):
    global news_text
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args:
            news_text = args
            save_json("news.json", news_text)
            await message.answer("✅ Новини оновлено!")
        else:
            await message.answer("⚠️ Напиши так: /setnews Текст_новин")
    else:
        await message.answer("⛔ У тебе нема прав міняти новини!")

# Ban
@dp.message_handler(commands=["ban"])
async def ban_user(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            user_id = int(message.get_args())
            if user_id not in BANNED:
                BANNED.append(user_id)
                save_json("banned.json", BANNED)
                await message.answer(f"✅ Користувач {user_id} забанений")
            else:
                await message.answer("⚠️ Він вже забанений")
        except:
            await message.answer("⚠️ Використання: /ban user_id")
    else:
        await message.answer("⛔ У тебе нема прав банити!")

# Unban
@dp.message_handler(commands=["unban"])
async def unban_user(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            user_id = int(message.get_args())
            if user_id in BANNED:
                BANNED.remove(user_id)
                save_json("banned.json", BANNED)
                await message.answer(f"✅ Користувач {user_id} розбанений")
            else:
                await message.answer("⚠️ Він і так не в бані")
        except:
            await message.answer("⚠️ Використання: /unban user_id")
    else:
        await message.answer("⛔ У тебе нема прав розбанювати!")

# Додати адміна
@dp.message_handler(commands=["setadmin"])
async def set_admin(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            user_id = int(message.get_args())
            if user_id not in ADMINS:
                ADMINS.append(user_id)
                save_json("admins.json", ADMINS)
                                await message.answer(f"✅ Користувач {user_id} тепер адмін")
            else:
                await message.answer("⚠️ Він вже адмін")
        except:
            await message.answer("⚠️ Використання: /setadmin user_id")
    else:
        await message.answer("⛔ У тебе нема прав додавати адмінів!")

# Видалити адміна
@dp.message_handler(commands=["deleteadmin"])
async def delete_admin(message: types.Message):
    if message.from_user.id in ADMINS:
        try:
            user_id = int(message.get_args())
            if user_id in ADMINS:
                ADMINS.remove(user_id)
                save_json("admins.json", ADMINS)
                await message.answer(f"✅ Користувач {user_id} більше не адмін")
            else:
                await message.answer("⚠️ Він і так не адмін")
        except:
            await message.answer("⚠️ Використання: /deleteadmin user_id")
    else:
        await message.answer("⛔ У тебе нема прав видаляти адмінів!")

# Отримати свій айді
@dp.message_handler(commands=["GetUserId"])
async def get_user_id(message: types.Message):
    await message.answer(f"🆔 Твій Telegram ID: {message.from_user.id}")

# ---------------------------
# Веб-сервер для Render/Replit
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
    keep_alive()
    executor.start_polling(dp, skip_updates=True)

