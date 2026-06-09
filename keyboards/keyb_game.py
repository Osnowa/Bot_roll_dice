from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_game_keyboard():
    '''Клавиатура для игры в кости'''
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Больше ⬆️', callback_data='roll_higher')],
            [InlineKeyboardButton(text='Меньше ⬇️', callback_data='roll_lower')],
            [InlineKeyboardButton(text='Одинаково 🟰', callback_data='roll_equal')]
        ]
    )

    return keyboard

def roll_dice_keyboard():
    """Клавиатура для броска кубика"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Бросить кубик 🎲', callback_data='roll_dice')]
        ]
    )
    return keyboard

def play_again_keyboard():
    '''Клавитура для повтроной игры'''
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='play_again')],
            [InlineKeyboardButton(text='Нет', callback_data='stop_game')]
        ]
    )

    return keyboard

def start_keyb():
    '''Клавиатура для комнанды старт'''
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Играть', callback_data='game')],
            [InlineKeyboardButton(text='Правила', callback_data='rules')],
            [InlineKeyboardButton(text='Статистика', callback_data='statistic')],
            [InlineKeyboardButton(text='Режим 3 подряд', callback_data='three_in_a_row')]
        ]
    )

    return keyboard

def start_game_three_a_row():
    '''Клавиатура для согласиня на игру 3 подряд'''
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вперед за победой !', callback_data='play_three_a_row')],
            [InlineKeyboardButton(text='Отказаться', callback_data='stop_three_a_row')]
        ]
    )

    return keyboard