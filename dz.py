from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
import database as db

# встановити ДЗ
@dp.message_handler(Command("setdz"))
async def set_dz_cmd(message: types.Message):
    args = message.get_args()
    if not args:
        return await message.reply("⚠️ Використання: /setdz [текст домашки]")

    db.set_dz(message.from_user.id, args)
    await message.reply(f"📘 Ваше ДЗ збережено: {args}")


# показати своє ДЗ
@dp.message_handler(Command("mydz"))
async def my_dz_cmd(message: types.Message):
    dz = db.get_dz(message.from_user.id)
    if not dz:
        return await message.reply("ℹ️ У вас немає збереженого ДЗ")
    await message.reply(f"📘 Ваше ДЗ: {dz}")


# видалити ДЗ
@dp.message_handler(Command("cleardz"))
async def clear_dz_cmd(message: types.Message):
    db.clear_dz(message.from_user.id)
    await message.reply("🗑️ Ваше ДЗ видалено")
