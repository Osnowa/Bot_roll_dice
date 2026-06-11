from sqlalchemy import BigInteger, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    u_score: Mapped["User_score"] = relationship("User_score", back_populates="user", uselist=False) # связь с таблицей очков, этой колонки на самом деле нет



class User_score(Base):
    '''Модель для хранения очков пользователей'''
    __tablename__ = 'users_score'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) # ключ пользователя
    u_id : Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True) # связь с таблицей пользователей
    score : Mapped[int] = mapped_column(Integer, default=1000) # очки по умолчанию 1000
    user: Mapped["User"] = relationship("User", back_populates="u_score")
    