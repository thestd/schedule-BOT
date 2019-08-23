from functools import wraps
from typing import Union

from aiogram import Dispatcher
from aiogram.utils.exceptions import Throttled
from aioredis import RedisConnection, create_connection

from app.core.config import REDIS_URL, REDIS_PORT, REDIS_DB

__all__ = ["Singleton", "RedisCache"]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)

        return cls._instances[cls]


class RedisCache:
    def __init__(self, url: str = REDIS_URL, port: int = REDIS_PORT,
                 db: int = REDIS_DB):
        self._url = url
        self._port = port
        self._db_id = db
        self._redis: Union[RedisConnection, None] = None

    async def _get_redis(self) -> RedisConnection:
        if not isinstance(self._redis, RedisConnection):
            self._redis = await create_connection((self._url, self._port),
                                                  db=self._db_id)

        return self._redis

    async def get_value(self, key: str) -> Union[None, str]:
        db = await self._get_redis()
        return await db.execute("get", key, encoding="utf-8")

    async def set_value(self, key: str, value: str, ex_time: int) -> None:
        db = await self._get_redis()
        await db.execute("set", key, value, "EX", ex_time)
