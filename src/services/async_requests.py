import asyncio
from typing import Union, List

from async_timeout import timeout

from src.adapters.external import AiohttpClient
from src.domain.async_requests import (
    RequestAsyncExecutor, get_response_json, to_seconds
)

URL = "https://exponea-engineering-assignment.appspot.com/api/work"


async def get_time(wait: int, first: bool = False) -> Union[List[dict], dict]:
    wait = to_seconds(wait)
    try:
        async with timeout(wait):
            async with AiohttpClient() as client:
                executor = RequestAsyncExecutor(first=first)
                tasks = await executor.run(client.get, URL)
                response = get_response_json(tasks)
                return response

    except asyncio.TimeoutError:
        return {}
