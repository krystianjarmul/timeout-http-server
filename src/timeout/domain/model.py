from dataclasses import dataclass
from enum import Enum
from typing import Union


class EventType(str, Enum):
    FAILED = "failed"
    ALL_SUCCESS = "all_success"
    FIRST_SUCCESS = "first_success"


@dataclass(frozen=True)
class Response:
    status_code: int
    body: Union[dict, str]
