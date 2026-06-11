from database.repository_db import UserRepository
from service.serv_user_db import UserService
import pytest

@pytest.mark.asyncio
async def test_register(session):
    '''Проверка на регистрацию нового пользователя'''
    repo = UserRepository(session)
    service = UserService(repo)

    # Проверяем, что будет при первом вызове
    result = await service.register(1, 'test_user')
    assert result == (False, None, 1000)

    # проверяем, что будет пользователь появился в базе
    user = await repo.get_user(1)
    assert user.username == 'test_user'
    assert user.telegram_id == 1

    score = await repo.get_score(1)
    assert score.score == 1000

    # Проверяем, что будет при втором вызове, когда пользователь есть в базе
    result2 = await service.register(1, 'test_user')

    user = await repo.get_user(1)

    assert result2 == (True, user, 1000)
