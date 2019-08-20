import motor.motor_asyncio

from app.core.utils import Singleton


class MongoStorage(metaclass=Singleton):
    def __init__(self, url):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self._db = self._client.pnu_bot

    async def update_user(self, user_id: int, **kwargs):
        await self._db.users.update_one({'id': user_id}, {'$set': kwargs})

    async def add_user(self, user_data: dict) -> dict:
        if "query" not in user_data:
            user_data["query"] = None
        if "query_type" not in user_data:
            user_data["query_type"] = None

        await self._db.users.insert_one(user_data)
        return user_data

    async def get_user(self, user_id: int) -> (dict, None):
        user = await self._db.users.find_one({'id': user_id})
        return user
