from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    game_id = State()
    game_code = State()
    game_role = State()
