from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database.models import Base
import pytest

@pytest.fixture
async def session():
    # создаем асинхронный движок
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
    ) 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # создаем асинхронную сессии
    async_session = async_sessionmaker(
        engine,
        expire_on_commit = False
        )
    
    # возвращаем асинхронную сессию для работы с базой данных
    async with async_session() as session:
        yield session

    # закрываем соединение
    await engine.dispose()