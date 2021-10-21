from http import HTTPStatus

import pytest

from src.timeout.adapters.external import AiohttpClient
from src.timeout.domain.async_requests import Response
from tests.fakes import FakeSession, FakeResponse, URL


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
        "To Many Requests"
    )
    session = FakeSession(fake_aiohttp_response)

    async with AiohttpClient(session) as client:
        response = await client.get(URL)

        assert response == Response(
            HTTPStatus.TOO_MANY_REQUESTS, "To Many Requests"
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


@pytest.mark.asyncio
async def test_aiohttp_client_get_raises_client_connection_error():
    fake_aiohttp_response = FakeResponse(HTTPStatus.REQUEST_TIMEOUT, None)
    session = FakeSession(fake_aiohttp_response)

    async with AiohttpClient(session) as client:
        response = await client.get(URL)

        assert response == Response(
            HTTPStatus.REQUEST_TIMEOUT, "Request Timeout"
        )
