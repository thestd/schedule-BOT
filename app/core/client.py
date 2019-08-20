from aiohttp import ClientSession

from app.core.config import api_url
from app.core.utils import Singleton


class ApiClient(metaclass=Singleton):
    def __init__(self, url: str = None):
        if url:
            self._api_url = url
        else:
            self._api_url = api_url
        self._session = ClientSession()

    async def group_predict(self, name):
        async with self._session.get(f"{self._api_url}/api/groups",
                                     params={"query": name}) as resp:
            return await resp.json()
