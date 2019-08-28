import ujson as json

from aiohttp import ClientSession

from app.core.config import API_URL, CACHE_TIME
from app.core.utils import Singleton, RedisCache

__all__ = ["ApiClient"]


class ApiClient(metaclass=Singleton):
    def __init__(self, storage: RedisCache, url: str = API_URL):
        self._cache = storage
        self._api_url = url
        self._session = ClientSession()

    async def _make_request(self, pred_type: str, params: dict) -> dict:
        """
        Makes request to schedule api with caching result
        """
        res = await self._cache.get_value(f"pred_type:{json.dumps(params)}")
        if not res:
            async with self._session.get(f"{self._api_url}/api/{pred_type}",
                                         params=params) as resp:
                res = await resp.json()
            await self._cache.set_value(f"pred_type:{json.dumps(params)}",
                                        json.dumps(res), CACHE_TIME)
            return res
        else:
            return json.loads(res)

    async def name_predict(self, q_type: str, name: str) -> dict:
        """
        Predicts name of group/teacher
        """
        # Just because `groups?query=ІПЗ-41` instead `group?query=ІПЗ-41`
        # Todo: fix Api url for name prediction `groups` -> `group` or some
        #  else
        return await self._make_request(f"{q_type}s", {"query": name})

    async def get_schedule(self, params: dict) -> dict:
        """
        Search schedule

        Args:
            params: will be passed to api request
                https://github.com/thestd/schedule-API
        """
        return await self._make_request("schedule", params)
