from database.models import User
from database.repository_db import UserRepository

class UserService:
    '''Сервис для работы с пользователем'''
    def __init__(self, user_repo: UserRepository):
        # получаем все методы репозитория user, которые работают с сессией
        self.user_repo = user_repo

    async def register(self, tg_id: int, user_name: str):
        '''Регистрируем пользователя'''
        user =  await self.user_repo.get_user(tg_id)
        if user:
            return True, user
        await self.user_repo.add_user(tg_id, username=user_name)
        return False, None
        