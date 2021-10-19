from typing import List, Union

from fastapi import FastAPI

from src.services import async_requests

app = FastAPI()


@app.get("/api/all")
async def get_all(time: int) -> Union[List[dict], dict]:
    response = await async_requests.get_time(wait=time)
    if not response:
        return {"detail": "error - timeout"}

    return response


@app.get("/api/first")
async def get_first(time: int) -> dict:
    response = await async_requests.get_time(wait=time, first=True)
    if not response:
        return {"detail": "error - timeout"}

    return response[0]
