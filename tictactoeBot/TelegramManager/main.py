from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils import executor

from db import *
from handlers import dp
from keyboards.reply_keyboard.buttons import menu_1



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    create_user(message.from_user.id, message.from_user.full_name)
    await message.reply("Привет! Я бот для игры в крестики-нолики!", reply_markup=menu_1)


if __name__ == '__main__':
    print('main')

    init_database()
    executor.start_polling(dp, skip_updates=True)

# btn_res = {1: "⭕",
#            2: "⭕",
#            3: "3",
#            4: "4",
#            5: "5",
#            6: "6",
#            7: "7",
#            8: "8",
#            9: "❌"
#            }

#
#     await message.reply(f"""
# ---------------
# - {chr(btn_res.get(1))} - {chr(btn_res.get(2))} - {chr(btn_res.get(3))} -
# -----------
# - {chr(btn_res.get(4))} - {chr(btn_res.get(5))} - {chr(btn_res.get(6))} -
# -----------
# - {chr(btn_res.get(7))} - {chr(btn_res.get(8))} - {chr(btn_res.get(9))} -
# ---------------
# """)
