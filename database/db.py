from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from database.models import Base
from config import DATABASE_URL

# Создаем асинхронный движок для подключения к базе данных
engine = create_async_engine(
    DATABASE_URL, 
    poll_size=5, # кол-во соединений в пуле
    max_overflow=10, # кол-во дополнительных соединений, которые могут быть созданы при превышении размера пула
    pool_pre_ping=True, # проверка соединения перед использованием
    echo=False
    )

# Создаем фабрику сессий для работы с базой данных
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    '''Создает таблицы в базе данных'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def dispose_engine():
    '''Закрывает соединение с базой данных'''
    await engine.dispose()