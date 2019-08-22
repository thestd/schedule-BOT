from typing import Union

from aioredis import RedisConnection, create_connection

from app.core.config import redis_url, redis_port, redis_db


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)

        return cls._instances[cls]


class RedisCache:
    def __init__(self, url: str = redis_url, port: int = redis_port,
                 db: int = redis_db):
        self._url = url
        self._port = port
        self._db_id = db
        self._db: Union[RedisConnection, None] = None

    async def get_db(self) -> RedisConnection:
        if not isinstance(self._db, RedisConnection):
            self._db = await create_connection((self._url, self._port),
                                               db=self._db_id)

        return self._db

    async def get_value(self, key: str) -> Union[None, str]:
        db = await self.get_db()
        return await db.execute("get", key, encoding="utf-8")

    async def set_value(self, key: str, value: str, ex_time: int) -> None:
        db = await self.get_db()
        await db.execute("set", key, value, "EX", ex_time)
