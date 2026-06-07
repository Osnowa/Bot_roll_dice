from random import randint

class Roll_dice:
    @staticmethod
    def roll():
        roll_1 = randint(1, 6)
        roll_2 = randint(1, 6)
        return roll_1, roll_2