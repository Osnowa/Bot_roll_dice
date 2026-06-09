from aiogram.fsm.state import State, StatesGroup

class FSMGame(StatesGroup):
    '''Состояния для игры в кости'''
    in_game = State() # ожидание броска кубика
    in_game_three_a_row = State() # режим игры 3 подряд

    