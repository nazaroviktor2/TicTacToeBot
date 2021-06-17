from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_start = KeyboardButton(text="Меню")
btn_back = KeyboardButton(text="Отмена")
menu_1 = ReplyKeyboardMarkup(resize_keyboard=True)
menu_1.row(btn_start)

menu_back = ReplyKeyboardMarkup(resize_keyboard=True)
menu_back.row(btn_back)






