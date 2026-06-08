from sqlalchemy import select, update
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

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

    async def update_game_st_win(self, tg_id:int):
        stmt = update(User).where(User.telegram_id == tg_id).values(win_game=User.win_game + 1, all_game=User.all_game + 1)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_game_st_lose(self, tg_id:int):
        stmt = update(User).where(User.telegram_id == tg_id).values(lose_game=User.lose_game + 1, all_game=User.all_game + 1)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_game_st_draw(self, tg_id:int):
        stmt = update(User).where(User.telegram_id == tg_id).values(draw_game=User.draw_game + 1, all_game=User.all_game + 1)
        await self.session.execute(stmt)
        await self.session.commit()


    async def get_static(self, tg_id: int):
        '''Получаем статистику игрока'''
        stmt = select(User).where(User.telegram_id == tg_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.warning(user)
        return user