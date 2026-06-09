from sqlalchemy import select, update
from database.models import User, User_score
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    """Репозиторий для работы с пользователем"""
    def __init__(self, session: AsyncSession):
        # передаем сессию в конструктор, что бы не создавать ее каждый раз при работе с базой данных
        self.session = session

    async def get_user(self, tg_id: int) -> User | None:  
        """Получить пользователя по id Telegram"""
        stmt = (
        select(User)
        .options(selectinload(User.u_score)) # загружаем связанный объект в запросе
        .where(User.telegram_id == tg_id)
        )
        result = await self.session.execute(stmt) # выполняем запрос к базе данных
        return result.scalar_one_or_none() # либо одного пользователя, либо None

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
        stmt = (select(User)
                .options(selectinload(User.u_score))
                .where(User.telegram_id == tg_id))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        logger.warning(user)
        return user
    
    async def add_score(self, user_id: int):
        '''Создаем запись в таблице с очками пользователя'''
        score = User_score(u_id=user_id)
        self.session.add(score)
        await self.session.commit()
        await self.session.refresh(score) # обновляем данные пользователся, что бы вставить id, который был сгенерирован

    async def get_score(self, user_id: int):
        '''Получаем таблицу с очками пользователя'''
        stmt = select(User_score).where(User_score.u_id == user_id)
        result = await self.session.execute(stmt)
        score = result.scalar_one_or_none()
        return score
    
    async def update_score(self, user_id: int, sc_res: int):
        stmt = update(User_score).where(User_score.u_id == user_id).values(score=User_score.score + sc_res)
        await self.session.execute(stmt)
        await self.session.commit()

