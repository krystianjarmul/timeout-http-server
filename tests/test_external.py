from http import HTTPStatus

from aiohttp import ContentTypeError
import pytest

from src.adapters.external import AiohttpClient
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
        return self._response


@pytest.mark.asyncio
async def test_aiohttp_client_get_returns_response_success():
    fake_aiohttp_response = FakeResponse(HTTPStatus.OK, {"time": 231})
    session = FakeSession(fake_aiohttp_response)

    async with AiohttpClient(session) as client:
        response = await client.get(URL)

        assert response == Response(HTTPStatus.OK, {"time": 231})


@pytest.mark.asyncio
async def test_aiohttp_client_get_returns_error_response_to_many_requests():
    fake_aiohttp_response = FakeResponse(
        HTTPStatus.TOO_MANY_REQUESTS,
        "To many requests"
    )
    session = FakeSession(fake_aiohttp_response)

    async with AiohttpClient(session) as client:
        response = await client.get(URL)

        assert response == Response(
            HTTPStatus.TOO_MANY_REQUESTS, "To many requests"
        )


@pytest.mark.asyncio
async def test_aiohttp_client_get_returns_error_response_server_error():
    fake_aiohttp_response = FakeResponse(
        HTTPStatus.TOO_MANY_REQUESTS,
        "Internal Server Error"
    )
    session = FakeSession(fake_aiohttp_response)

    async with AiohttpClient(session) as client:
        response = await client.get(URL)

        assert response == Response(
            HTTPStatus.TOO_MANY_REQUESTS, "Internal Server Error"
        )
