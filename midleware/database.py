from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class DatabaseMiddleware(BaseMiddleware):
    '''Мидлвар для работы с базой данных'''
    def __init__(self, factory: async_sessionmaker):
        self.factory = factory

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
        ) -> Any:
        
        async with self.factory() as session:
            data['session'] = session # положили сессию в словарь, который будет доступен в каждом хендлере
            result = await handler(event, data)
            # сессия будет закрыта
        return result