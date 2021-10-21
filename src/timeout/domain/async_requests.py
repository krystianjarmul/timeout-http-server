from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from contextlib import suppress
from http import HTTPStatus
from typing import List

from src.timeout.domain.model import Response


def get_json(responses: List[Response]) -> List[dict]:
    return [
        response.body for response in responses
        if response.status_code == HTTPStatus.OK
    ]


class AbstractAsyncExecutor(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _run(self, fn, *args, **kwargs) -> List[Response]:
        raise NotImplementedError

    async def run(self, fn, *args, **kwargs) -> List[Response]:
        return await self._run(fn, *args, **kwargs)


class RequestAsyncExecutor(AbstractAsyncExecutor):
    def __init__(self, first: bool = False):
        self._first = first
        self._when = self._get_when()
        self._amount = 2

    async def _run(self, fn, *args, **kwargs):
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

    def _get_when(self) -> str:
        if self._first:
            return asyncio.FIRST_COMPLETED
        return asyncio.ALL_COMPLETED
