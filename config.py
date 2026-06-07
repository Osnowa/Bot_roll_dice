from environs import Env
from dataclasses import dataclass

env = Env()
env.read_env()

@dataclass
class Config:
    BOT_TOKEN: str = env.str("BOT_TOKEN")
    POSTGRES_USER: str = env.str("POSTGRES_USER")
    POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD")
    POSTGRES_DB: str = env.str("POSTGRES_DB")
    PGADMIN_DEFAULT_EMAIL: str = env.str("PGADMIN_DEFAULT_EMAIL")
    PGADMIN_DEFAULT_PASSWORD: str = env.str("PGADMIN_DEFAULT_PASSWORD")
    DB_HOST: str = env.str("DB_HOST")
    DB_PORT: int = env.int("DB_PORT")
    REDIS_HOST: str = env.str("REDIS_HOST")
    REDIS_PORT: int = env.int("REDIS_PORT")
