import json

from aiohttp import ClientSession

from app.core.config import api_url, cached_time
from app.core.utils import Singleton, RedisCache


class ApiClient(metaclass=Singleton):
    def __init__(self, storage: RedisCache, url: str = api_url):
        self.storage = storage
        self._api_url = url
        self._session = ClientSession()

    async def _predict(self, pred_type: str, params: dict):
        res = await self.storage.get_value(f"pred_type:{json.dumps(params)}")
        if not res:
            async with self._session.get(f"{self._api_url}/api/{pred_type}",
                                         params=params) as resp:
                res = await resp.json()
            await self.storage.set_value(f"pred_type:{json.dumps(params)}",
                                         json.dumps(res), cached_time)
            return res
        else:
            return json.loads(res)

    async def group_predict(self, name: str):
        return await self._predict("groups", {"query": name})

    async def teacher_predict(self, name: str):
        return await self._predict("teachers", {"query": name})

    async def get_schedule(self, params: dict):
        return await self._predict("schedule", params)
