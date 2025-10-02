from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
import database as db

MAIN_ADMIN_ID = 7618560125  # 🔴 заміни на свій ID

# додати адміна
@dp.message_handler(Command("addAdmin"))
async def add_admin_cmd(message: types.Message):
    if message.from_user.id != MAIN_ADMIN_ID:
        return await message.reply("⛔ Тільки головний адмін може додавати!")

    args = message.get_args()
    if not args.isdigit():
        return await message.reply("⚠️ Використання: /addAdmin [id]")

    user_id = int(args)
    db.add_admin(user_id)
    await message.reply(f"✅ {user_id} тепер адмін!")


# видалити адміна
@dp.message_handler(Command("deleteAdmin"))
async def delete_admin_cmd(message: types.Message):
    if message.from_user.id != MAIN_ADMIN_ID:
        return await message.reply("⛔ Немає доступу!")

    args = message.get_args()
    if not args.isdigit():
        return await message.reply("⚠️ Використання: /deleteAdmin [id]")

    user_id = int(args)
    db.delete_admin(user_id)
    await message.reply(f"❌ {user_id} видалено з адмінів")


# показати свій id
@dp.message_handler(Command("infoId"))
async def info_id(message: types.Message):
    await message.reply(
        f"👤 Ваш ID: `{message.from_user.id}`\n📛 Username: @{message.from_user.username or 'немає'}",
        parse_mode="Markdown"
    )
