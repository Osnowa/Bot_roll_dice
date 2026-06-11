import pytest
from service.game_service_result import get_game_result

@pytest.mark.parametrize(
    "roll_igr, roll_opponenta, choise_igr, expected_result", 
    [
        (5,4,'roll_higher', 'win'),
        (5,4,'roll_lower', 'lose'),
        (5,4,'roll_equal', 'lose'),
        (4,5,'roll_higher', 'lose'),
        (4,5,'roll_lower', 'win'),
        (4,5,'roll_equal', 'lose'),
        (4,4,'roll_higher', 'lose'),
        (4,4,'roll_lower', 'lose'),
        (4,4,'roll_equal', 'win')
    ]
)
def test_game_result(roll_igr, roll_opponenta, choise_igr, expected_result):
    assert get_game_result(roll_igr, roll_opponenta, choise_igr) == expected_result

