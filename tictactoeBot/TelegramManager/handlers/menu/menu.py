import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from db import find_open_game, get_second_role, update_game_second_id, set_game_status_player_joining
from handlers.menu.create_game import send_create_game_open
from handlers.menu.join_game import send_user_join
from keyboards.inline.buttons import keyboard_menu, keyboard_create_game, keyboard_join_game_back
from loader import dp

from keyboards.reply_keyboard.buttons import menu_back
from states import GameState


@dp.message_handler(text='Меню')
@dp.message_handler(commands=['menu'])
async def send_menu(message: types.Message):
    await message.answer("Меню", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Что вы хотете сделать?", reply_markup=keyboard_menu)


@dp.callback_query_handler(text="menu:create_game")
async def send_create_game(call: CallbackQuery):
    logging.info(f"call = {call.data}")
    await call.message.edit_text(
        f"Вы хотите создать игру\nКакую игру выхотите создать? Открытую для всех или закрутую",
        reply_markup=keyboard_create_game)


@dp.callback_query_handler(text="menu:find_game")
async def send_find_game(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f"call = {call.data}")
    await call.message.edit_text(f"Поиск игры ...")
    game_id = find_open_game()
    if game_id is None:
        await call.message.answer("На данный момент нет созданых игр")
        await send_create_game_open(call, state)

    else:
        game_id = game_id[0]
        logging.info(f"id = {game_id}")

        update_game_second_id(game_id, call.from_user.id)
        async with state.proxy() as data:
            data['game_id'] = game_id
            data['game_role'] = get_second_role(game_id)
        await call.message.answer(f"Вы присоединились к игре - {game_id}. Ожидайте начало")
        set_game_status_player_joining(game_id)
        await send_user_join(game_id, call.from_user.full_name)


@dp.callback_query_handler(text="menu:join_game")
async def send_join_game(call: CallbackQuery):
    logging.info(f"call = {call.data}")
    await call.message.edit_text(f"Вы хотите присоединится к игре")
    await call.message.answer("Введите код игры", reply_markup=menu_back)
    await GameState.game_code.set()
