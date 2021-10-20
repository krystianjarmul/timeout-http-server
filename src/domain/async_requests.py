from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from contextlib import suppress
from dataclasses import dataclass
from typing import List
from http import HTTPStatus


def get_json(responses: List[Response]) -> List[dict]:
    return [
        response.json
        for response in responses
        if response.status_code == HTTPStatus.OK
    ]


@dataclass(frozen=True)
class Response:
    status_code: int
    json: dict


class AbstractAsyncExecutor(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _run(self, fn, *args, **kwargs):
        raise NotImplementedError

    async def run(self, fn, *args, **kwargs):
        return await self._run(fn, *args, **kwargs)


class RequestAsyncExecutor(AbstractAsyncExecutor):
    def __init__(self, first: bool = False):
        self.first = first
        self.when = asyncio.FIRST_COMPLETED if first else asyncio.ALL_COMPLETED

    async def _run(self, fn, *args, **kwargs) -> List[Response]:
        tasks = [fn(*args, **kwargs) for _ in range(2)]
        done, pending = await asyncio.wait(tasks, return_when=self.when)

        if pending:
            await self._cancel_pending(pending)

        responses = [task.result() for task in done]
        return responses

    @staticmethod
    async def _cancel_pending(pending: set):
        gather = asyncio.gather(*pending)
        gather.cancel()

        with suppress(asyncio.CancelledError):
            await gather
