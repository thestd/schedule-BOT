from datetime import datetime, timedelta
from typing import Union, Optional

from aioredis import RedisConnection, create_connection, create_redis_pool, Redis

from app.core.config import REDIS_URL, REDIS_PORT, REDIS_DB, TIME_ZONE

__all__ = ["Singleton", "RedisCache", "Date"]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)

        return cls._instances[cls]


class RedisCache:
    __slots__ = ("_url", "_port", "_db_id", "_redis", "_uri")

    def __init__(self, url: str = REDIS_URL, port: int = REDIS_PORT,
                 db: int = REDIS_DB, uri=None):
        self._url = url
        self._port = port
        self._db_id = db
        self._uri = uri
        self._redis: Union[RedisConnection, None] = None

    async def _get_redis(self) -> RedisConnection:
        if not self._redis or self._redis.closed:
            if self._uri:
                self._redis = await create_redis_pool(self._uri)
            else:
                self._redis = await create_connection((self._url, self._port),
                                                      db=self._db_id)

        return self._redis

    async def get_value(self, key: str) -> Union[None, str]:
        db = await self._get_redis()
        return await db.execute("get", key, encoding="utf-8")

    async def set_value(self, key: str, value: str, ex_time: int) -> None:
        db = await self._get_redis()
        await db.execute("set", key, value, "EX", ex_time)

    async def flush_database(self) -> None:
        db = await self._get_redis()
        await db.execute("flushall")


class Date:
    __slots__ = ("_day", "_week_start_date")

    def __init__(self, date: Optional[Union[str, datetime, None]] = None):
        """
        :param str date: date in format `week_start:day`
        """
        if isinstance(date, str):
            week_start_date, day = date.split(":")
            self._week_start_date = datetime.strptime(
                week_start_date,
                "%d.%m.%Y"
            )
            self._day = int(day)
        elif isinstance(date, datetime):
            self._day = date.weekday()
            self._week_start_date = date - timedelta(self._day)
        else:
            self._day = datetime.now(TIME_ZONE).weekday()
            self._week_start_date = datetime.now(TIME_ZONE) - timedelta(self._day)

    def shift_week(self, days):
        self._week_start_date += timedelta(days)

    @property
    def as_db_str(self) -> str:
        str_week = self._week_start_date.strftime("%d.%m.%Y")
        return f"{str_week}:{self._day}"

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, value):
        self._day = int(value)

    @property
    def week_start_day(self) -> datetime:
        return self._week_start_date

    @week_start_day.setter
    def week_start_day(self, value):
        self.week_start_day = value

    @property
    def as_date(self) -> datetime:
        return self._week_start_date + timedelta(self._day)

    @property
    def as_string(self) -> str:
        return self.as_date.strftime("%d.%m.%Y")
