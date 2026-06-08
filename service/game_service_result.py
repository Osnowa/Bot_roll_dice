# Отвечает за работу с результатами игры


def get_game_result(roll_igroka : int, roll_oponenta: int, choise_igroka: str) -> str:
    if (roll_igroka > roll_oponenta and choise_igroka == 'roll_higher') or (roll_igroka < roll_oponenta and choise_igroka == 'roll_lower') or (roll_igroka == roll_oponenta and choise_igroka == 'roll_equal'):
        return 'win'
    else:
        return 'lose'