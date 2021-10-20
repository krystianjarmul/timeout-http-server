from http import HTTPStatus

from aiohttp import ContentTypeError, ClientConnectionError

from src.adapters.external import AbstractAsyncClient
from src.domain.async_requests import AbstractAsyncExecutor
from src.domain.async_requests import Response

URL = "https://exponea-engineering-assignment.appspot.com/api/work"


class FakeResponse:
    def __init__(self, status, body):
        self.status = status
        self._body = body

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def json(self):
        if not isinstance(self._body, dict):
            raise ContentTypeError(None, None)
        return self._body

    async def text(self):
        return self._body


class FakeSession:
    def __init__(self, response):
        self._response = response

    async def close(self):
        pass

    def get(self, url):
        if self._response.status == HTTPStatus.REQUEST_TIMEOUT:
            raise ClientConnectionError
        return self._response


class FakeAsyncClient(AbstractAsyncClient):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _get(self, url):
        return Response(200, {"time": 200})

    async def _parse_response(self, response):
        pass


class FakeAsyncExecutor(AbstractAsyncExecutor):

    def __init__(self, first=False):
        self._first = first
        self._response = None

    def set_response(self, response):
        self._response = response

    async def _run(self, fn, *args, **kwargs):
        if not self._first:
            return self._response
        return self._response[0:1]
