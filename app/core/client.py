from aiohttp import ClientSession

from app.core.config import api_url
from app.core.utils import Singleton


class ApiClient(metaclass=Singleton):
    def __init__(self, url: str = None):
        if url:
            self._api_url = url
        else:
            self._api_url = api_url
        self._schedule_url = f"{self._api_url}/api/schedule"
        self._session = ClientSession()

    async def _predict(self, name, pred_type):
        async with self._session.get(f"{self._api_url}/api/{pred_type}",
                                     params={"query": name}) as resp:
            return await resp.json()

    async def group_predict(self, name):
        return await self._predict(name, "groups")

    async def teacher_predict(self, name):
        return await self._predict(name, "teachers")

    async def get_schedule(self, **kwargs):
        async with self._session.get(self._schedule_url, params=kwargs) as res:
            return await res.json()
