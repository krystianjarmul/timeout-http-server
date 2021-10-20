from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from contextlib import suppress
from dataclasses import dataclass
from typing import List, Union
from http import HTTPStatus


def get_json(responses: List[Response]) -> List[dict]:
    return [
        response.body
        for response in responses
        if response.status_code == HTTPStatus.OK
    ]


@dataclass(frozen=True)
class Response:
    status_code: int
    body: Union[dict, str]


class AbstractAsyncExecutor(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _run(self, fn, *args, **kwargs):
        raise NotImplementedError

    async def run(self, fn, *args, **kwargs):
        return await self._run(fn, *args, **kwargs)


class RequestAsyncExecutor(AbstractAsyncExecutor):
    def __init__(self, first: bool = False):
        self._first = first
        self._when = asyncio.FIRST_COMPLETED if first else asyncio.ALL_COMPLETED
        self._amount = 2

    async def _run(self, fn, *args, **kwargs) -> List[Response]:
        tasks = [fn(*args, **kwargs) for _ in range(self._amount)]
        done, pending = await asyncio.wait(tasks, return_when=self._when)

        if pending:
            await self._cancel_pending(pending)

        done = self._break_the_tie(done)

        responses = [task.result() for task in done]
        return responses

    @staticmethod
    async def _cancel_pending(pending: set):
        gather = asyncio.gather(*pending)
        gather.cancel()

        with suppress(asyncio.CancelledError):
            await gather

    def _break_the_tie(self, done: set) -> set:
        if self._first and len(done) > 1:
            return {next(iter(done))}
        return done
