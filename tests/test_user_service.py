import pytest
from unittest.mock import AsyncMock, Mock
from service.serv_user_db import UserService
from config import Config_game

conf_game = Config_game()

@pytest.mark.asyncio
async def test_user_service_gameresult_win():
    repo = AsyncMock()
    service = UserService(repo) # создаем экземпляр сервиса, у которого есть все методы репозитория
    await service.process_game_result(1, 'win', 1)
    repo.update_game_st_win.assert_awaited_once_with(1)
    repo.update_score.assert_awaited_once_with(1, conf_game.score_win)
    repo.update_game_st_lose.assert_not_awaited()
 
@pytest.mark.asyncio
async def test_user_service_gameresult_lose():
    repo = AsyncMock()
    service = UserService(repo)
    await service.process_game_result(1, 'lose', 1)
    repo.update_game_st_lose.assert_awaited_once_with(1)
    repo.update_score.assert_awaited_once_with(1, -conf_game.score_win)

@pytest.mark.asyncio
async def test_user_service_gameresult_draw():
    repo = AsyncMock()
    service = UserService(repo)
    await service.process_game_result(1, 'draw', 1)
    repo.update_game_st_draw.assert_awaited_once_with(1)
    repo.update_score.assert_awaited_once_with(1, conf_game.score_win_draw)

@pytest.mark.asyncio
async def test_user_service_register():
    '''Проверяем, что при регистрации существующего пользователя, возвращает True, пользователя и его очки'''
    repo = AsyncMock()

    # создаем пользователя в репозитории
    user = Mock()
    user.id = 1
    user.telegram_id = 1
    user.username = 'test_user'

    user.u_score = Mock()
    user.u_score.score = 1000

    service = UserService(repo)
    
    # подменяем метод get_user
    repo.get_user.return_value = user

    result = await service.register(1, 'test_user')
    assert result == (True, user, 1000)
    repo.get_user.assert_awaited_once_with(1) # убедимся, что метод get_user был вызван один раз
    repo.add_user.assert_not_awaited() # убедимся, что метод add_user не был вызван
    repo.add_score.assert_not_awaited() # убедимся, что метод add_score не был вызван
    repo.get_score.assert_not_awaited() # убедимся, что метод get_score не был вызван


@pytest.mark.asyncio
async def test_user_service_register_new_user(mocker):
    '''Проверрка на регистрацию нового пользователя'''
    repo = AsyncMock()
    service = UserService(repo)

    user = Mock()
    user.id = 1
    user.telegram_id = 1
    user.username = 'test_user'

    user.u_score = Mock()
    user.u_score.score = 1000

    repo.get_user.side_effect = [None, user, user]
   
    score = Mock()
    score.score = 1000
    repo.get_score.return_value = score

    # Проверяем, что будет при первом вызове функции register
    result = await service.register(1, 'test_user')
    assert result == (False, None, 1000)
    repo.add_user.assert_awaited_once_with(1, username='test_user') # убедимся, что метод add_user был вызван один раз c нашим именем

    # проверяем, что будет при втором вызове
    result2 = await service.register(1, 'test_user')
    assert result2 == (True, user, 1000)

   