from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

@dataclass
class Config:
    BOT_TOKEN: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int

    @classmethod
    def from_env(cls):
        return cls(
            BOT_TOKEN=env.str("BOT_TOKEN"),
            POSTGRES_USER=env.str("POSTGRES_USER"),
            POSTGRES_PASSWORD=env.str("POSTGRES_PASSWORD"),
            POSTGRES_DB=env.str("POSTGRES_DB"),
            PGADMIN_DEFAULT_EMAIL=env.str("PGADMIN_DEFAULT_EMAIL"),
            PGADMIN_DEFAULT_PASSWORD=env.str("PGADMIN_DEFAULT_PASSWORD"),
            DB_HOST=env.str("DB_HOST"),
            DB_PORT=env.int("DB_PORT"),
            REDIS_HOST=env.str("REDIS_HOST"),
            REDIS_PORT=env.int("REDIS_PORT"),
        )

@dataclass
class Config_game:
    '''Конфигурация очков игры'''
    score_game: int = 100
    score_win: int = score_game * 2
    score_win_draw: int = score_game * 3
    score_win_three_in_a_row: int = score_game * 10
