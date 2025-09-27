import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from flask import Flask, request

# 🔑 Токен від BotFather
API_TOKEN = "8065465326:AAEV8aYGEEgDyWZwPZikBJIwl7LkB99TU5I"

# 📡 Дані для webhook
WEBHOOK_HOST = "https://dashboard.render.com/web/srv-d3bpkvt6ubrc73e9tu8g/events"  # заміни на свій домен Render
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# 🔧 Налаштування сервера
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))

# список айді адмінів
ADMINS = [7618560125]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# тут зберігається домашнє завдання
homework_text = "Домашнє завдання ще не встановлено ❌"

# список забанених користувачів
banned_users = set()


# ---------------------------
# Фільтр: ігнор забанених
# ---------------------------
@dp.message_handler(lambda message: message.from_user.id in banned_users)
async def block_banned(message: types.Message):
    await message.answer("⛔ Ти забанений у цьому боті!")


# ---------------------------
# Команди
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


@dp.message_handler(commands=["ban"])
async def ban_user(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔ У тебе нема прав!")

    args = message.get_args()
    if not args.isdigit():
        return await message.answer("⚠️ Використовуй так: /ban userid")

    user_id = int(args)
    banned_users.add(user_id)
    await message.answer(f"✅ Користувач {user_id} забанений.")


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
        await message.answer(f"✅ Користувач {user_id} розбанений.")
    else:
        await message.answer("ℹ️ Цей користувач і так не забанений.")


# ---------------------------
# Webhook хендлери
# ---------------------------
async def on_startup(dp):
    # ставимо webhook
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    # прибираємо webhook
    await bot.delete_webhook()


# ---------------------------
# Запуск бота через webhook
# ---------------------------
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
