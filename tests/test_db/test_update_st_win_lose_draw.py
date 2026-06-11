from database.repository_db import UserRepository
import pytest

@pytest.mark.asyncio
async def test_update_game_st_win(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')

    user = await repo.get_user(1)
    assert user.win_game == 0
    assert user.all_game == 0
    
    await repo.update_game_st_win(1)
    
    user = await repo.get_user(1)
    
    assert user.win_game == 1
    assert user.all_game == 1

@pytest.mark.asyncio
async def test_update_game_st_lose(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')

    user = await repo.get_user(1)
    assert user.lose_game == 0
    assert user.all_game == 0
    
    await repo.update_game_st_lose(1)
    
    user = await repo.get_user(1)
    
    assert user.lose_game == 1
    assert user.all_game == 1

@pytest.mark.asyncio
async def test_update_game_st_draw(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')

    user = await repo.get_user(1)
    assert user.draw_game == 0
    assert user.all_game == 0
    
    await repo.update_game_st_draw(1)
    
    user = await repo.get_user(1)
    
    assert user.draw_game == 1
    assert user.all_game == 1