import json
from aiogram import Bot, Dispatcher, executor, types
from flask import Flask
from threading import Thread

# 🔑 Встав сюди свій токен від BotFather
API_TOKEN = "8065465326:AAEV8aYGEEgDyWZwPZikBJIwl7LkB99TU5I"

# список айді адмінів
ADMINS = [7618560125]  # заміни на свій Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# тут зберігається домашнє завдання
homework_text = "Домашнє завдання ще не встановлено ❌"

# ---------------------------
# Бан-лист (з файлу)
# ---------------------------
BAN_FILE = "banlist.json"

def load_bans():
    try:
        with open(BAN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_bans():
    with open(BAN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(banned_users), f)

banned_users = load_bans()


# ---------------------------
# Фільтр: ігнор забанених
# ---------------------------
@dp.message_handler(lambda message: message.from_user.id in banned_users)
async def block_banned(message: types.Message):
    await message.answer("⛔ Ти забанений у цьому боті!")


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
# Команда /ban
# ---------------------------
@dp.message_handler(commands=["ban"])
async def ban_user(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔ У тебе нема прав!")

    args = message.get_args()
    if not args.isdigit():
        return await message.answer("⚠️ Використовуй так: /ban userid")

    user_id = int(args)
    banned_users.add(user_id)
    save_bans()
    await message.answer(f"✅ Користувач {user_id} забанений.")


# ---------------------------
# Команда /unban
# ---------------------------
@dp.message_handler(commands=["unban"])
async def unban_user(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔ У тебе нема прав!")

    args = message.get_args()
    if not args.isdigit():
        return await message.answer("⚠️ Використовуй так: /unban userid")

    user_id = int(args)
    if user_id in banned_users:
        banned_users.remove(user_id)
        save_bans()
        await message.answer(f"✅ Користувач {user_id} розбанений.")
    else:
        await message.answer("ℹ️ Цей користувач і так не забанений.")


# ---------------------------
# Веб-сервер (щоб Render/Replit не засинав)
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
