from typing import List, Union

from fastapi import FastAPI
from aiohttp import ClientSession

from src.domain.async_requests import RequestAsyncExecutor
from src.adapters.external import AiohttpClient
from src.service_layer.async_requests import ExponeaHttpTestingClient

app = FastAPI()
URL = "https://exponea-engineering-assignment.appspot.com/api/work"


@app.get("/api/all")
async def get_all(time: int) -> Union[List[dict], dict]:
    session = ClientSession()
    client = ExponeaHttpTestingClient(
        AiohttpClient(session),
        RequestAsyncExecutor(),
        time
    )
    response = await client.get(URL)
    if not response:
        return {"detail": "error - timeout"}

    return response


@app.get("/api/first")
async def get_first(time: int) -> dict:
    session = ClientSession()
    client = ExponeaHttpTestingClient(
        AiohttpClient(session),
        RequestAsyncExecutor(),
        time,
        first=True
    )
    response = await client.get(URL)
    if not response:
        return {"detail": "error - timeout"}

    return response[0]
