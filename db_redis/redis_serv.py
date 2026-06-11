from redis.asyncio import Redis
from config import Config

config = Config.from_env()
# Создаем асинхронное соединение с Redis
redis_db = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)