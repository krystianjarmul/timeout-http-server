import asyncio
from typing import Union, List, Type

from async_timeout import timeout

from src.adapters.external import AbstractAsyncClient
from src.domain.async_requests import get_json, AbstractAsyncExecutor


class ExponeaHttpTestingClient:
    def __init__(
        self,
        async_client: AbstractAsyncClient,
        async_executor: AbstractAsyncExecutor,
        wait_time: int,
        first: bool = False,
    ):
        self._async_client = async_client
        self._async_executor = async_executor
        self._wait_time = self._to_seconds(wait_time)
        self._first = first

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
