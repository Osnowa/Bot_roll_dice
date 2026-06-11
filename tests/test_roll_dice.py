from service.game_service import Roll_dice


def test_roll_dice():
    assert len(Roll_dice.roll()) == 2
    for e in range(10):
        roll_1, roll_2 = Roll_dice.roll()
        assert 1 <= roll_1 <= 6
        assert 1 <= roll_2 <= 6

def test_roll(mocker):
    mocker.patch('service.game_service.randint', side_effect=[3, 5])
    assert Roll_dice.roll() == (3, 5)