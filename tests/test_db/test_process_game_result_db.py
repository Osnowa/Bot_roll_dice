from database.repository_db import UserRepository
from service.serv_user_db import UserService
import pytest

@pytest.mark.asyncio
async def test_process_game_result_win(session):
    repo = UserRepository(session)
    service = UserService(repo)
    await service.register(1, 'test_user')

    await service.process_game_result(1, 'win', 1)
    user = await repo.get_user(1)
    assert user.win_game == 1
    assert user.all_game == 1
    assert user.u_score.score == 1200

@pytest.mark.asyncio
async def test_process_game_result_lose(session):
    repo = UserRepository(session)
    service = UserService(repo)
    await service.register(1, 'test_user')

    await service.process_game_result(1, 'lose', 1)
    user = await repo.get_user(1)
    assert user.win_game == 0
    assert user.lose_game == 1
    assert user.all_game == 1
    assert user.u_score.score == 800

@pytest.mark.asyncio
async def test_process_game_result_draw(session):
    repo = UserRepository(session)
    service = UserService(repo)
    await service.register(1, 'test_user')

    await service.process_game_result(1, 'draw', 1)
    user = await repo.get_user(1)
    assert user.win_game == 0
    assert user.draw_game == 1
    assert user.all_game == 1
    assert user.u_score.score == 1300

@pytest.mark.asyncio
async def test_process_game_result_win_three_in_a_row(session):
    repo = UserRepository(session)
    service = UserService(repo)
    await service.register(1, 'test_user')

    await service.process_game_result(1, 'win_three_in_a_row', 1)
    user = await repo.get_user(1)
    assert user.win_game == 1
    assert user.all_game == 1
    assert user.u_score.score == 2000