from abc import ABC, abstractmethod
import asyncio
from asyncio import Task
from contextlib import suppress
from dataclasses import dataclass
from typing import Set, List
from http import HTTPStatus


def get_response_json(tasks: Set[Task]) -> List[dict]:
    return [
        task.result().json for task in tasks
        if task.result().status_code == HTTPStatus.OK
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

    async def _run(self, fn, *args, **kwargs):
        tasks = [fn(*args, **kwargs) for _ in range(2)]
        done, pending = await asyncio.wait(tasks, return_when=self.when)

        if pending:
            await self._cancel_pending(pending)

        return done

    @staticmethod
    async def _cancel_pending(pending: set):
        gather = asyncio.gather(*pending)
        gather.cancel()

        with suppress(asyncio.CancelledError):
            await gather
