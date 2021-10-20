import asyncio
import pytest
from asynctest import patch

from src.domain.async_requests import Response
from src.service_layer.async_requests import ExponeaHttpTestingClient

from .fakes import FakeAsyncClient, FakeAsyncExecutor, URL


@pytest.mark.asyncio
async def test_http_testing_client_success_all_responses():
    fake_async_client = FakeAsyncClient()
    fake_executor = FakeAsyncExecutor()
    fake_executor.set_response(
        [Response(200, {"time": 320}), Response(200, {"time": 320})]
    )

    client = ExponeaHttpTestingClient(
        fake_async_client, fake_executor, wait_time=1000
    )
    response_json = await client.get(URL)

    assert response_json == [{"time": 320}, {"time": 320}]


@pytest.mark.asyncio
async def test_http_testing_client_success_first_response():
    fake_async_client = FakeAsyncClient()
    fake_executor = FakeAsyncExecutor(first=True)
    fake_executor.set_response(
        [Response(200, {"time": 320}), Response(200, {"time": 320})]
    )

    client = ExponeaHttpTestingClient(
        fake_async_client, fake_executor, wait_time=1000
    )
    response_json = await client.get(URL)

    assert response_json == [{"time": 320}]


@pytest.mark.asyncio
async def test_http_testing_client_success_all_responses_one_failed():
    fake_async_client = FakeAsyncClient()
    fake_executor = FakeAsyncExecutor()
    fake_executor.set_response(
        [Response(200, {"time": 320}), Response(500, "Internal Server Error")]
    )

    client = ExponeaHttpTestingClient(
        fake_async_client, fake_executor, wait_time=1000
    )
    response_json = await client.get(URL)

    assert response_json == [{"time": 320}]


@pytest.mark.asyncio
async def test_http_testing_client_success_all_responses_one_failed():
    fake_async_client = FakeAsyncClient()
    fake_executor = FakeAsyncExecutor()
    fake_executor.set_response(
        [Response(200, {"time": 320}), Response(500, "Internal Server Error")]
    )

    with patch(
            "src.service_layer.async_requests.timeout",
            side_effect=asyncio.TimeoutError
    ):
        client = ExponeaHttpTestingClient(
            fake_async_client, fake_executor, wait_time=100
        )
        response_json = await client.get(URL)

        assert response_json == {}
