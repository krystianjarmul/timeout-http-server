from src.adapters.external import AbstractAsyncClient
from src.domain.async_requests import Response


class FakeAsyncClient(AbstractAsyncClient):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _get(self, url):
        return Response(200, {"time": 200})

    async def _parse_response(self, response):
        pass
