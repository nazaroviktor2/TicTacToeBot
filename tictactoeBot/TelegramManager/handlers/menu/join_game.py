import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from exception import NotFoundGame
from handlers.game.move import send_board
from keyboards.inline.buttons import keyboard_menu,  keyboard_create_game_ready
from keyboards.reply_keyboard.buttons import menu_back
from loader import dp, bot
from states import GameState
from db import get_game_id_by_code, update_game_second_id, get_players_id, \
    get_second_role, set_game_status_starting, set_game_status_player_joining


async def send_user_join(id_game, name):
    first_id, second_id = get_players_id(id_game)
    logging.info(f"First id = {first_id} , second id = {second_id}")
    await bot.send_message(first_id, f"{name} присоединился к вашей игре! Готовы начать? ",
                           reply_markup=keyboard_create_game_ready)


@dp.message_handler(state=GameState.game_code)
async def send_get_game_code(message: types.Message, state: FSMContext):
    code = message.text
    logging.info(f"Code = {code}")
    if code == "Отмена":
        await message.answer(f"Вход в игру отменен", reply_markup= ReplyKeyboardRemove())
        await state.finish()
        await message.answer("Что вы хотите сделать?", reply_markup=keyboard_menu)
    else:
        code = code.upper()
        try:
            game_id = get_game_id_by_code(str(code))
            logging.info(f"id = {game_id}")
            update_game_second_id(game_id, message.from_user.id)
            await state.finish()
            async with state.proxy() as data:
                data['game_id'] = game_id
                data['game_role'] = get_second_role(game_id)
            set_game_status_player_joining(game_id)
            await message.answer(f"Вы присоединились к игре - {game_id}. Ожидайте начало", reply_markup=ReplyKeyboardRemove())

            await send_user_join(game_id, message.from_user.full_name)

        except NotFoundGame:
            await message.reply(f"Не верный код. Повторите попытку", reply_markup=menu_back)
            await GameState.game_code.set()


@dp.callback_query_handler(text="join_game:start")
async def send_start_join(call: CallbackQuery, state: FSMContext):
    logging.info(f"call = {call.data}")
    async with state.proxy() as data:
        id_game = data.get('game_id')
    set_game_status_starting(id_game)
    await send_board(id_user=call.from_user.id, id_game=id_game)


@dp.callback_query_handler(text="join_game:back")
async def send_back_join(call: CallbackQuery, state: FSMContext):
    logging.info(f"call = {call.data}")
    await call.message.edit_text(f"Вход в игру отменен")
    await call.message.answer("Меню", reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await call.message.answer("Что вы хотите сделать?", reply_markup=keyboard_menu)
