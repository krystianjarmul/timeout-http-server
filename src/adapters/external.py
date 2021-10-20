from abc import ABC, abstractmethod

from aiohttp import ContentTypeError

from src.domain.async_requests import Response


class AbstractAsyncClient(ABC):
    async def get(self, url: str) -> Response:
        return await self._get(url)

    @abstractmethod
    async def _get(self, url: str):
        raise NotImplementedError

    @abstractmethod
    async def _parse_response(self, response) -> Response:
        raise NotImplementedError


class AiohttpClient(AbstractAsyncClient):

    def __init__(self, session):
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def _get(self, url):
        async with self._session.get(url) as response:
            return await self._parse_response(response)

    async def _parse_response(self, response):
        status = response.status
        try:
            body = await response.json()
        except ContentTypeError:
            body = await response.text()
        return Response(status, body)
