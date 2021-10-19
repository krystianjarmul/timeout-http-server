from typing import List, Union

from fastapi import FastAPI

from src.service.main import main

app = FastAPI()


@app.get("/api/all")
async def get_all(time: int) -> Union[List[dict], dict]:
    response = await main(time=time)
    if not response:
        return {"error": "timeout"}

    return response


@app.get("/api/first")
async def get_first(time: int) -> dict:
    response = await main(time=time, first=True)
    if not response:
        return {"error": "timeout"}

    return response[0]
