from typing import List, Union

from aiohttp import ClientSession
from fastapi import FastAPI, Response, status

from src.domain.async_requests import RequestAsyncExecutor
from src.adapters.external import AiohttpClient
from src.service_layer.async_requests import ExponeaHttpTestingClient

app = FastAPI()
URL = "https://exponea-engineering-assignment.appspot.com/api/work"


@app.get("/api/all", status_code=status.HTTP_200_OK)
async def get_all(time: int, response: Response) -> Union[List[dict], dict]:
    session = ClientSession()
    client = ExponeaHttpTestingClient(
        AiohttpClient(session),
        RequestAsyncExecutor(),
        time
    )
    exp_response = await client.get(URL)
    if not exp_response:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return {"detail": "error - timeout"}

    return exp_response


@app.get("/api/first", status_code=status.HTTP_200_OK)
async def get_first(time: int, response: Response) -> dict:
    session = ClientSession()
    client = ExponeaHttpTestingClient(
        AiohttpClient(session),
        RequestAsyncExecutor(),
        time
    )
    exp_response = await client.get(URL)
    if not exp_response:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return {"detail": "error - timeout"}

    return exp_response[0]
