from sqlalchemy import BigInteger, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    '''Модель для хранения информации о пользователях'''
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) # ключ пользователя
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False) # id пользователя в Telegram
    username: Mapped[str| None] = mapped_column(nullable=True) # имя пользователя в Telegram
    all_game: Mapped[int] = mapped_column(default=0) # всего игр
    win_game: Mapped[int] = mapped_column(default=0) # выигранных игр
    lose_game: Mapped[int] = mapped_column(default=0) # проигранных игр
    draw_game: Mapped[int] = mapped_column(default=0) # ничьих игр

