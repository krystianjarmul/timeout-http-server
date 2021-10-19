from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import asyncio
from aiohttp import ClientSession




@dataclass(frozen=True)
class Response:
    status_code: int
    json: dict



class AbstractAsyncClient(ABC):

    async def get(self, url: str) -> Response:
        response = await self._get(url)
        return response

    @abstractmethod
    async def _get(self, url: str):
        raise NotImplementedError


class AioHttpAsyncClient:

    def __aenter__(self):
        self._session = ClientSession()
        return self

    # def __await__(self):
    #     return self.new_sleep().__await__()

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._session = None

    async def get(self, url: str):
        async with self._session.get(url) as response:
            return await self._parse_response(response)

    @staticmethod
    async def new_sleep():
        await asyncio.sleep(2)

    @staticmethod
    async def _parse_response(response) -> Response:
        status_code = response.status
        body = await response.json()
        return Response(status_code, body)
