from dataclasses import dataclass

from typing import List

from timeout.domain.model import EventType


class Event:
    pass


@dataclass
class Result(Event):
    event_type: EventType
    timeout: int


@dataclass
class AllSuccess(Result):
    times: List[str]


@dataclass
class FirstSuccess(Result):
    time: str


@dataclass
class Failed(Result):
    error: str
