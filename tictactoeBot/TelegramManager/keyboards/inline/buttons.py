from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import move_callback, menu_callback, create_game_callback, \
    join_game_callback

keyboard_move = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data=move_callback.new("one")),
            InlineKeyboardButton(text="2", callback_data=move_callback.new("two")),
            InlineKeyboardButton(text="3", callback_data=move_callback.new("three")),
        ],
        [
            InlineKeyboardButton(text="4", callback_data=move_callback.new("four")),
            InlineKeyboardButton(text="5", callback_data=move_callback.new("five")),
            InlineKeyboardButton(text="6", callback_data=move_callback.new("six")),
        ],
        [
            InlineKeyboardButton(text="7", callback_data=move_callback.new("seven")),
            InlineKeyboardButton(text="8", callback_data=move_callback.new("eight")),
            InlineKeyboardButton(text="9", callback_data=move_callback.new("nine")),
        ], [
            InlineKeyboardButton(text="Сдаться", callback_data=move_callback.new("loss"))
        ]

    ]
)

btn_find_game = InlineKeyboardButton("Найти игру", callback_data=menu_callback.new("find_game"))
btn_create_game = InlineKeyboardButton("Создать игру", callback_data=menu_callback.new("create_game"))
btn_join_game = InlineKeyboardButton("Присоединиться к игре", callback_data=menu_callback.new("join_game"))

keyboard_menu = InlineKeyboardMarkup().row(btn_find_game).add(btn_create_game).add(btn_join_game)

btn_create_open_game = InlineKeyboardButton("Открытую", callback_data=create_game_callback.new("open"))
btn_create_close_game = InlineKeyboardButton("Закрытую", callback_data=create_game_callback.new("close"))

keyboard_create_game = InlineKeyboardMarkup().row(btn_create_open_game).row(btn_create_close_game)
keyboard_create_game_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data=create_game_callback.new("back"))]
])

keyboard_join_game_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data=join_game_callback.new("back"))]
])
keyboard_join_game_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать", callback_data=join_game_callback.new("start"))]
])


keyboard_create_game_ready = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Начать", callback_data=create_game_callback.new("start"))]])
