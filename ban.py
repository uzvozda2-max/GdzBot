from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
import database as db

# бан
@dp.message_handler(Command("ban"))
async def ban_user(message: types.Message):
    args = message.get_args()
    if not args.isdigit():
        return await message.reply("⚠️ Використання: /ban [id]")

    user_id = int(args)
    db.add_ban(user_id)
    await message.reply(f"🚫 Користувач {user_id} забанений")


# розбан
@dp.message_handler(Command("unban"))
async def unban_user(message: types.Message):
    args = message.get_args()
    if not args.isdigit():
        return await message.reply("⚠️ Використання: /unban [id]")

    user_id = int(args)
    db.remove_ban(user_id)
    await message.reply(f"✅ Користувач {user_id} розбанений")


# показати банліст
@dp.message_handler(Command("banlist"))
async def show_banlist(message: types.Message):
    bans = db.get_bans()
    if not bans:
        return await message.reply("✅ Банліст порожній")
    text = "🚫 Забанені:\n" + "\n".join([str(uid) for uid in bans])
    await message.reply(text)
