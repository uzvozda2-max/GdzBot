import json
import os
from aiogram import Bot, Dispatcher, executor, types
from flask import Flask
from threading import Thread

# 🔑 Токен від BotFather
API_TOKEN = "8065465326:AAEV8aYGEEgDyWZwPZikBJIwl7LkB99TU5I"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ---------------------------
# Завантаження / Збереження
# ---------------------------
def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_json(filename, default)
        return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# завантажуємо дані
ADMINS = load_json("admins.json", [7618560125, 6964713379])  # твій айді тут
BANNED = load_json("banned.json", [])
if os.path.exists("dz.txt"):
    with open("dz.txt", "r", encoding="utf-8") as f:
        homework_text = f.read().strip()
else:
    homework_text = "Домашнє завдання ще не встановлено ❌"


# ---------------------------
# Команди
# ---------------------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id in BANNED:
        return await message.answer("⛔ Тебе забанено!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📚 Домашнє завдання")
    await message.answer("Привіт! 👋\nЩо тобі треба?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "📚 Домашнє завдання")
async def show_homework(message: types.Message):
    if message.from_user.id in BANNED:
        return await message.answer("⛔ Тебе забанено!")
    await message.answer(f"📌 Домашнє завдання:\n\n{homework_text}")


@dp.message_handler(commands=["setdz"])
async def set_homework(message: types.Message):
    global homework_text
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args:
            homework_text = args
            with open("dz.txt", "w", encoding="utf-8") as f:
                f.write(homework_text)
            await message.answer("✅ Домашнє завдання оновлено!")
        else:
            await message.answer("⚠️ Напиши так: /setdz Текст_завдання")
    else:
        await message.answer("⛔ У тебе нема прав міняти ДЗ!")


# ---------------------------
# Адмінські команди
# ---------------------------

@dp.message_handler(commands=["ban"])
async def ban_user(message: types.Message):
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args.isdigit():
            user_id = int(args)
            if user_id not in BANNED:
                BANNED.append(user_id)
                save_json("banned.json", BANNED)
                await message.answer(f"✅ Користувача {user_id} забанено!")
            else:
                await message.answer("⚠️ Він вже у бані!")
        else:
            await message.answer("⚠️ Використовуй так: /ban user_id")
    else:
        await message.answer("⛔ У тебе нема прав банити!")


@dp.message_handler(commands=["unban"])
async def unban_user(message: types.Message):
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args.isdigit():
            user_id = int(args)
            if user_id in BANNED:
                BANNED.remove(user_id)
                save_json("banned.json", BANNED)
                await message.answer(f"✅ Користувача {user_id} розбанено!")
            else:
                await message.answer("⚠️ Він не в бані!")
        else:
            await message.answer("⚠️ Використовуй так: /unban user_id")
    else:
        await message.answer("⛔ У тебе нема прав розбанювати!")


@dp.message_handler(commands=["setadmin"])
async def set_admin(message: types.Message):
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args.isdigit():
            user_id = int(args)
            if user_id not in ADMINS:
                ADMINS.append(user_id)
                save_json("admins.json", ADMINS)
                await message.answer(f"✅ Користувача {user_id} додано в адміни!")
            else:
                await message.answer("⚠️ Він вже адмін!")
        else:
            await message.answer("⚠️ Використовуй так: /setadmin user_id")
    else:
        await message.answer("⛔ У тебе нема прав додавати адмінів!")


@dp.message_handler(commands=["deleteadmin"])
async def delete_admin(message: types.Message):
    if message.from_user.id in ADMINS:
        args = message.get_args()
        if args.isdigit():
            user_id = int(args)
            if user_id in ADMINS:
                ADMINS.remove(user_id)
                save_json("admins.json", ADMINS)
                await message.answer(f"✅ Користувача {user_id} видалено з адмінів!")
            else:
                await message.answer("⚠️ Він не адмін!")
        else:
            await message.answer("⚠️ Використовуй так: /deleteadmin user_id")
    else:
        await message.answer("⛔ У тебе нема прав видаляти адмінів!")


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
