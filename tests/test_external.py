from typing import Union

import asyncio
from asynctest import patch, CoroutineMock
import pytest

from src.adapters.external import AioHttpAsyncClient

url = "https://exponea-engineering-assignment.appspot.com/api/work"


def set_get_mock(get_mock, status: int, body: Union[str, dict]):
    get_mock.return_value.__aenter__.return_value.status = status
    get_mock.return_value.__aenter__.return_value.json = CoroutineMock(
        return_value=body
    )


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_aiohttp_client_get_url_success(get_mock):
    set_get_mock(get_mock, 200, {"time": 300})

    client = AioHttpAsyncClient()
    response = await client.get(url)

    assert response.status_code == 200
    assert response.body == {"time": 300}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_aiohttp_client_get_url_success_multi_requests(get_mock):
    set_get_mock(get_mock, 200, {"time": 300})

    client = AioHttpAsyncClient()
    tasks = [client.get(url) for _ in range(15)]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
        assert response.body == {"time": 300}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_aiohttp_client_get_url_success_multi_requests(get_mock):
    set_get_mock(get_mock, 200, {"time": 300})

    client = AioHttpAsyncClient()
    tasks = [client.get(url) for _ in range(15)]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
        assert response.body == {"time": 300}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_aiohttp_client_get_url_failed_internal_server_error(get_mock):
    set_get_mock(get_mock, 500, "Internal Server Error")

    client = AioHttpAsyncClient()
    response = await client.get(url)

    assert response.status_code == 500
    assert response.body == "Internal Server Error"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_aiohttp_client_get_url_failed_too_many_requests(get_mock):
    set_get_mock(get_mock, 429, "Too many requests")

    client = AioHttpAsyncClient()
    response = await client.get(url)

    assert response.status_code == 429
    assert response.body == "Too many requests"
