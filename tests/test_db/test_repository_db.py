from database.repository_db import UserRepository
import pytest

@pytest.mark.asyncio
async def test_add_user(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')

    user = await repo.get_user(1)
    assert user.username == 'ilya'
    assert user.telegram_id == 1

@pytest.mark.asyncio
async def test_update_score(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')
    await repo.add_score(1)

    score = await repo.get_score(1)
    assert score.score == 1000

    await repo.update_score(1, 100)
    score_update = await repo.get_score(1)
    assert score_update.score == 1100

@pytest.mark.asyncio
async def test_get_user(session):
    repo = UserRepository(session)
    await repo.add_user(1, username = 'ilya')
    await repo.add_score(1)

    user = await repo.get_user(1)
    assert user.username == 'ilya'
    assert user.telegram_id == 1
    assert user.u_score.score == 1000

@pytest.mark.asyncio
async def test_get_user_not_found(session):
    repo = UserRepository(session)
    user = await repo.get_user(1)
    assert user is None

@pytest.mark.asyncio
async def test_get_score_not_found(session):
    repo = UserRepository(session)
    score = await repo.get_score(1)
    assert score is None
