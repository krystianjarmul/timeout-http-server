import asyncio
from typing import Union, List

from aiohttp import ClientSession
from async_timeout import timeout

from src.adapters.external import AbstractAsyncClient, AiohttpClient
from src.domain.async_requests import (
    get_json, AbstractAsyncExecutor, RequestAsyncExecutor
)


class HttpTestingClient:
    def __init__(
            self,
            async_client: AbstractAsyncClient,
            async_executor: AbstractAsyncExecutor,
            wait_time: int,
    ):
        self._async_client = async_client
        self._async_executor = async_executor
        self._wait_time = self._to_seconds(wait_time)

    async def get(self, url: str) -> Union[List[dict], dict]:
        try:
            async with timeout(self._wait_time):
                async with self._async_client as client:
                    executor = self._async_executor
                    responses = await executor.run(client.get, url)
                    response_json = get_json(responses)
                    return response_json

        except asyncio.TimeoutError:
            return {}

    @staticmethod
    def _to_seconds(time: int) -> float:
        return time / 1000


async def get_response(url: str, time: int) -> Union[List[dict], dict]:
    session = ClientSession()
    client = HttpTestingClient(
        AiohttpClient(session),
        RequestAsyncExecutor(),
        time
    )
    response = await client.get(url)
    return response