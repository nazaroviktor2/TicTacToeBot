import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import typing

from db import get_board_by_id, update_board, get_board_cross_id, get_board_zero_id, set_game_status_finished, \
    game_set_winner
from keyboards.inline.callback_datas import move_callback
from loader import dp, bot
from keyboards.inline.buttons import keyboard_move, keyboard_menu


# btn_res = {1: 49,
#            2: 50,
#            3: 51,
#            4: 52,
#            5: 53,
#            6: 54,
#            7: 55,
#            8: 56,
#            9: 57
#            }


def get_board(id_game):
    one, two, three, four, five, six, seven, eight, nine = get_board_by_id(id_game)
    btn_res = {"one": one,
               "two": two,
               "three": three,
               "four": four,
               "five": five,
               "six": six,
               "seven": seven,
               "eight": eight,
               "nine": nine,
               }

    return btn_res


async def send_board(id_user: int, id_game):
    btn_res = get_board(id_game)
    logging.info(btn_res)
    await bot.send_message(id_user, text=
    f"""
 -----------------
 - {btn_res.get('one')} - {btn_res.get('two')} - {btn_res.get('three')} -
 -----------------
 - {btn_res.get('four')} - {btn_res.get('five')} - {btn_res.get('six')} -
 -----------------
 - {btn_res.get('seven')} - {btn_res.get('eight')} - {btn_res.get('nine')} -
 -----------------
 """,
                           reply_markup=keyboard_move)


# @dp.message_handler(commands=['test'])
# async def send_board_test(message: types.Message):
#
#     await message.answer(text=
#                          f"""
#  -----------------
#  - {chr(btn_res.get(1))} - {chr(btn_res.get(2))} - {chr(btn_res.get(3))} -
#  -----------------
#  - {chr(btn_res.get(4))} - {chr(btn_res.get(5))} - {chr(btn_res.get(6))} -
#  -----------------
#  - {chr(btn_res.get(7))} - {chr(btn_res.get(8))} - {chr(btn_res.get(9))} -
#  -----------------
#  """,
#                          reply_markup=keyboard_move)

def check_win(data, role: str):
    if data.get("one") == role and data.get("two") == role and data.get("three") == role:
        return True

    elif data.get("four") == role and data.get("five") == role and data.get("six") == role:
        return True

    elif data.get("seven") == role and data.get("eight") == role and data.get("nine") == role:
        return True

    elif data.get("one") == role and data.get("five") == role and data.get("nine") == role:
        return True

    elif data.get("three") == role and data.get("five") == role and data.get("seven") == role:
        return True

    elif data.get("one") == role and data.get("four") == role and data.get("seven") == role:
        return True

    elif data.get("two") == role and data.get("five") == role and data.get("eight") == role:
        return True

    elif data.get("three") == role and data.get("six") == role and data.get("nine") == role:
        return True

    else:
        return False


def check_draw(data):
    if '1' in data.values() or '2' in data.values() or '3' in data.values() or '4' in data.values() \
            or '5' in data.values() or '6' in data.values() or '7' in data.values() or '8' in data.values() or '9' in data.values():
        return False
    else:
        return True


async def get_state(state: FSMContext):
    async with state.proxy() as data:
        game_id = data.get('game_id')
        game_role = data.get('game_role')
    return game_id, game_role


@dp.callback_query_handler(
    move_callback.filter(item_name=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']))
async def move(call: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    logging.info(f"call = {call.data}")
    item_name = callback_data.get('item_name')
    logging.info(f"item_name = {item_name}")

    async with state.proxy() as data:
        game_id = data.get('game_id')
        game_role = data.get('game_role')
    logging.info(f"game_id = {game_id}, game_role = {game_role}")
    btn_res = get_board(game_id)
    if btn_res.get(item_name) != 'X' and btn_res.get(item_name) != 'O':

        if game_role == "cross":
            update_board(board_id=game_id, position=item_name, value="X")
            await call.message.edit_text(f"Вы походили на поле {item_name}")
            if check_win(get_board(game_id), role='X'):
                await call.message.answer(f"Крестик победил!", reply_markup=keyboard_menu)
                await bot.send_message(get_board_zero_id(game_id), "Крестик победил!", reply_markup=keyboard_menu)
                set_game_status_finished(game_id)
                game_set_winner(game_id=game_id, user_id=call.from_user.id)
                await state.finish()
            elif check_draw(get_board(game_id)):
                await call.message.answer("Ничья!", reply_markup=keyboard_menu)
                await bot.send_message(get_board_zero_id(game_id), "Ничья!", reply_markup=keyboard_menu)
                set_game_status_finished(game_id)
                await state.finish()

            else:
                await call.message.answer("Ход соперника")
                await send_board(get_board_zero_id(game_id), game_id)

        elif game_role == "zero":
            update_board(board_id=game_id, position=item_name, value="O")
            await call.message.edit_text(f"Вы походили на поле {item_name}. Ход соперника")
            if check_win(get_board(game_id), role='O'):
                await call.message.answer(f"Нолик победил!",reply_markup=keyboard_menu )
                await bot.send_message(get_board_cross_id(game_id), "Нолик победил!", reply_markup=keyboard_menu)
                set_game_status_finished(game_id)
                game_set_winner(game_id=game_id, user_id=call.from_user.id)
                await state.finish()
            elif check_draw(get_board(game_id)):
                await call.message.answer("Ничья!",  reply_markup=keyboard_menu)
                await bot.send_message(get_board_cross_id(game_id), "Ничья!", reply_markup=keyboard_menu)
                set_game_status_finished(game_id)
                await state.finish()

            else:
                await send_board(get_board_cross_id(game_id), game_id)
        else:
            await call.message.answer("У вас нет роли в игре")
    else:
        await call.message.edit_text(f"Поле {item_name} уже занято выбирете другое поле", reply_markup="")
        await send_board(call.from_user.id, game_id)


@dp.callback_query_handler(move_callback.filter(item_name='loss'))
async def move_loss(call: CallbackQuery, state: FSMContext ):
    await call.answer(cache_time=60)
    logging.info(f"call = {call.data}")
    await call.message.edit_text(f"Вы сдались")
    async with state.proxy() as data:
        game_id = data.get('game_id')
        game_role = data.get('game_role')
    if game_role == 'cross':
        await call.message.answer(f"Нолик победил!", reply_markup=keyboard_menu)
        zero_id = get_board_zero_id(game_id)
        await bot.send_message(zero_id, "Противник сдался! Нолик победил!", reply_markup=keyboard_menu)
        set_game_status_finished(game_id)

        game_set_winner(game_id=game_id, user_id=zero_id)
        await state.finish()

    elif game_role == "zero":
        await call.message.answer(f"Крестик победил!", reply_markup=keyboard_menu)
        cross_id = get_board_cross_id(game_id)
        await bot.send_message(cross_id, "Противник сдался! Крестик победил!", reply_markup=keyboard_menu)
        set_game_status_finished(game_id)

        game_set_winner(game_id=game_id, user_id=cross_id)
        await state.finish()
