import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import Config
from keyboards.menu import set_main_menu
from database.db import create_tables, dispose_engine, SessionFactory
from midleware.database import DatabaseMiddleware
from handlers.hand_game import router as game_router
from handlers.hand_command import router as command_router
from db_redis.redis_serv import redis_db

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger.info("Старт бота")

    config = Config()

    storage = RedisStorage(redis=redis_db) # используем уже созданное соединение с Redis из redis_serv.py

    async with Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode="HTML")
        ) as bot:

        dp = Dispatcher(storage=storage)

        # Регистрируем роутеры
        logger.info("Регистрируем роутеры")
        dp.include_router(game_router) # роутер для игры в кости
        dp.include_router(command_router) # роутер для команд

        # Регистрируем мидлвари 
        dp.update.middleware(DatabaseMiddleware(SessionFactory)) # мидлвари на каждое обновление, 
        # для работы с база данных по ключу 'session', передаем фабрику сессий,
        # закрывается автоматически после обработки обновления

        await create_tables() # создаем таблицы в базе данных

        await set_main_menu(bot) # добавляем главное меню бота
        # reload - на время разработки
        await bot.delete_webhook(drop_pending_updates=True) # делаем так, что бы бот не получал старые сообщения, которые были отправлены ему, пока он был оффлайн

        try:
            logger.info("Бот запущен")
            # reload - на время разработки
            await dp.start_polling(bot, reload = True)
        finally:
            await dispose_engine() # закрываем соединение с базой данных
            await bot.session.close() # закрываем сессию бота
            logger.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())