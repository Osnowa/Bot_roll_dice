from sqlalchemy import select, update
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """Репозиторий для работы с пользователем"""
    def __init__(self, session: AsyncSession):
        # передаем сессию в конструктор, что бы не создавать ее каждый раз при работе с базой данных
        self.session = session

    async def get_user(self, tg_id: int):
        """Получить пользователя по id Telegram"""
        stmt = select(User).where(User.telegram_id == tg_id)
        result = await self.session.execute(stmt) # выполняем запрос к базе данных
        user = result.scalar_one_or_none() # либо одного пользователя, либо None
        return user

    async def add_user(self, tg_id: int, username: str = None):
        """Добавить пользователя"""
        user = User(telegram_id=tg_id, username=username)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user) # обновляем данные пользователся, что бы вставить id, который был сгенерирован

    # Добавить методы для обновления игры
    