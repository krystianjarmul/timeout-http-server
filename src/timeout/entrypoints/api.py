from typing import List, Union

from fastapi import FastAPI, Response, status

from src.timeout.domain.events import AllSuccess, Failed, FirstSuccess
from src.timeout.domain.model import EventType
from src.timeout.entrypoints.redis_publisher import publish
from src.timeout.service_layer.services import get_response

app = FastAPI()
URL = "https://exponea-engineering-assignment.appspot.com/api/work"


@app.get("/api/all", status_code=status.HTTP_200_OK)
async def get_all(timeout: int, response: Response) -> Union[List[dict], dict]:
    exp_response = await get_response(URL, timeout)

    if not exp_response:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        publish("timeout", Failed(EventType.FAILED, timeout, "error"))
        return {"detail": "error - timeout"}

    results = [str(result["time"]) for result in exp_response]
    publish("timeout", AllSuccess(EventType.ALL_SUCCESS, timeout, results))
    return exp_response


@app.get("/api/first", status_code=status.HTTP_200_OK)
async def get_first(timeout: int, response: Response) -> dict:
    exp_response = await get_response(URL, timeout)

    if not exp_response:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        publish("timeout", Failed(EventType.FAILED, timeout, "timeout error"))
        return {"detail": "error - timeout"}

    result = str(exp_response[0]["time"])
    publish("timeout", FirstSuccess(EventType.FIRST_SUCCESS, timeout, result))
    return exp_response[0]
