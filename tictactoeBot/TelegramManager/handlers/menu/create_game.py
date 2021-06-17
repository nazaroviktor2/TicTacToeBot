import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from exception import NotFoundGame
from keyboards.inline.buttons import keyboard_create_game_back, keyboard_menu
from loader import dp, bot
from db import create_game, get_game_code_by_id, delete_game, create_board, get_players_id, get_first_role, \
    get_second_role, set_game_status_starting, get_game_status
from handlers.game.move import send_board


@dp.callback_query_handler(text="create_game:start")
async def start_game(call: CallbackQuery, state: FSMContext):

    await call.answer(cache_time=60)
    logging.info(f"call = {call.data}")
    async with state.proxy() as data:
        id_game = data.get('game_id')
    if id_game is None:
        await call.message.edit_text("Игра не найдена")
    else:
        try:
            status = get_game_status(id_game)

            if status == "player joining":

                set_game_status_starting(id_game)
                first_id, second_id = get_players_id(id_game)
                first_role = get_first_role(id_game)
                second_role = get_second_role(id_game)
                logging.info(f"First id = {first_id} role = {first_role} , second id = {second_id}  role = {second_role}")
                if first_role == 'cross':
                    cross_id = first_id
                    zero_id = second_id
                else:
                    cross_id = second_id
                    zero_id = first_id
                create_board(id=id_game, cross_id=cross_id, zero_id=zero_id)

                if first_role == 'cross':
                    await call.message.answer("Игра создана ! Вы играйте за крестик", reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(second_id, "Вы играйте за нолик ! Ожидайте хода соперника")

                    await call.message.answer("Ваш ход")
                    await send_board(call.from_user.id, id_game)
                else:
                    await call.message.answer("Игра создана! Вы играйте за нолик!")
                    await call.message.answer("Ожидайте хода соперника")
                    await bot.send_message(second_id, "Вы играйте за крестик! Ваш ход ")
                    await send_board(second_id, id_game)

            elif status == "finished":
                await call.message.edit_text("Игра уже закончилась")
            elif status == "starting":
                await call.message.edit_text("Игра уже началась")
            else:
                await call.message.edit_text("Невозможно начать")
        except NotFoundGame as e:
            print(e)
            await call.message.edit_text("Игра не найдена")


@dp.callback_query_handler(text="create_game:open")
async def send_create_game_open(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f"call = {call.data}")
    game_id = create_game(call.from_user.id, True)
    game_code = get_game_code_by_id(game_id)
    async with state.proxy() as data:
        data['game_id'] = game_id
        data['game_code'] = game_code
        data['game_role'] = get_first_role(game_id)
    logging.info(f"game_id = {game_id}")
    game_code = get_game_code_by_id(game_id)
    await call.message.edit_text(
        f"Создана открытая игра. Ожидайте когда кто-нибудь присоединиться.\n"
        f"Код игры - {game_code}",
        reply_markup=keyboard_create_game_back)


@dp.callback_query_handler(text="create_game:close")
async def send_create_game_close(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f"call = {call.data}")
    game_id = create_game(call.from_user.id, False)
    game_code = get_game_code_by_id(game_id)
    async with state.proxy() as data:
        data['game_id'] = game_id
        data['game_code'] = game_code
        data['game_role'] = get_first_role(game_id)

    await call.message.edit_text(
        f"Создана закрытая игра. Скажите код игры вашему другу чтобы он мог присоединиться\n"
        f"Код игры - {game_code}",
        reply_markup=keyboard_create_game_back)


@dp.callback_query_handler(text="create_game:back")
async def send_create_game_back(call: CallbackQuery, state: FSMContext):
    logging.info(f"call = {call.data}")
    async with state.proxy() as data:
        game_id = data.get('game_id')

    logging.info(f"id game = {game_id}")
    status = get_game_status(game_id)

    if status == "find players":
        await call.message.edit_text(f"Игра отменена")
        await state.finish()
        await call.message.answer("Меню", reply_markup=ReplyKeyboardRemove())
        await call.message.answer(f"Что вы хотете сделать?", reply_markup=keyboard_menu)
        delete_game(game_id)

    elif status == "player joining":
        await call.message.edit_text(f"Игра отменена")
        await state.finish()
        await call.message.answer("Меню", reply_markup=ReplyKeyboardRemove())
        await call.message.answer(f"Что вы хотете сделать?", reply_markup=keyboard_menu)
        first_id, second_id = get_players_id(game_id)
        await bot.send_message(second_id, "Игрок отменил игру. Найдите другую игру ", reply_markup=keyboard_menu)
        delete_game(game_id)

    elif status == "finished":
        await call.message.edit_text("Не возможно отменить игру. Игра закончина")

    elif status == "starting":
        await call.message.edit_text("Не возможно отменить игру. Игра уже идет")
