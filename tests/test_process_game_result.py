import pytest
from unittest.mock import AsyncMock, Mock
from service.serv_user_db import UserService


@pytest.mark.asyncio
async def test_process_game_result(mocker):
    repo = AsyncMock()
    service = UserService(repo)
    
    config = Mock()
    config.score_win = 10
    config.score_win_draw = 5

    mocker.patch('service.serv_user_db.Config_game', return_value = config)

    await service.process_game_result(1, 'win', 1)
    repo.update_game_st_win.assert_awaited_once_with(1)
    repo.update_score.assert_awaited_once_with(1, config.score_win)
    repo.update_game_st_lose.assert_not_awaited()
    repo.update_game_st_draw.assert_not_awaited()