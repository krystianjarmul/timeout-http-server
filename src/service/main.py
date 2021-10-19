import asyncio
from asyncio import Task
from dataclasses import dataclass
from enum import Enum
from contextlib import suppress
from typing import List, Set

import aiohttp
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError, ClientResponse
from async_timeout import timeout

URL = "https://exponea-engineering-assignment.appspot.com/api/work"


@dataclass(frozen=True)
class Response:
    status_code: int
    json: dict


class Status(Enum):
    FAILED = 0
    SUCCESS = 1


def to_seconds(ms: int) -> float:
    return ms / 1000


async def create_response(response: ClientResponse) -> Response:
    status_code = response.status
    try:
        data = await response.json()
    except ContentTypeError:
        data = await response.text()
    return Response(status_code, data)


async def get_response(session: ClientSession) -> Response:
    async with session.get(URL) as client_response:
        response = await create_response(client_response)
        return response


async def cancel_pending(pending: set):
    gather = asyncio.gather(*pending)
    gather.cancel()

    with suppress(asyncio.CancelledError):
        await gather


async def send_request(first=False) -> Set[Task]:
    async with aiohttp.ClientSession() as session:
        done, pending = await asyncio.wait(
            [get_response(session) for _ in range(2)],
            return_when=asyncio.FIRST_COMPLETED
            if first else asyncio.ALL_COMPLETED
        )

        if pending:
            await cancel_pending(pending)

        return done


def get_responses(tasks: Set[Task]) -> List[Response]:
    return [
        task.result()
        if task.result().status_code == 200 else {}
        for task in tasks
    ]


async def main():
    expected_time = to_seconds(1000)
    try:
        async with timeout(expected_time):
            results = await send_request(first=True)
            return get_responses(results)

    except asyncio.TimeoutError:
        return {}


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    try:
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
