from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

import requests


@dataclass(frozen=True)
class Response:
    status_code: int
    body: dict


class AbstractClient(ABC):

    def get(self, url: str) -> Response:
        response = self._get(url)
        status_code, body = self._parse_response(response)
        return Response(status_code, body)

    @abstractmethod
    def _get(self, url: str):
        raise NotImplementedError

    @abstractmethod
    def _parse_response(self, response) -> Tuple[int, dict]:
        raise NotImplementedError


class RequestsClient(AbstractClient):

    def _get(self, url):
        return requests.get(url)

    def _parse_response(self, response):
        status_code = response.status_code
        body = response.json()
        return status_code, body
