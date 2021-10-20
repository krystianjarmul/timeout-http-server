import asyncio

import pytest

from src.domain.async_requests import Response, get_json, RequestAsyncExecutor

test_delay = 0.01


async def get_test_task():
    global test_delay
    test_delay += 0.01
    await asyncio.sleep(test_delay)
    return Response(200, {"time": 300})


async def get_test_task_tie():
    await asyncio.sleep(0.01)
    return Response(200, {"time": 300})


def test_get_response_json_returns_all_success_responses():
    responses = [
        Response(200, {"time": 231}), Response(200, {"time": 323})
    ]
    response_json = get_json(responses)

    assert response_json == [{"time": 231}, {"time": 323}]


def test_get_response_json_returns_only_one_success_responses():
    responses = [
        Response(200, {"time": 231}), Response(500, "Internal Server Error")
    ]
    response_json = get_json(responses)

    assert response_json == [{"time": 231}]


def test_get_response_json_returns_empty_list_if_all_responses_failed():
    responses = [
        Response(429, "To many requests"),
        Response(500, "Internal Server Error")
    ]
    response_json = get_json(responses)

    assert response_json == []


@pytest.mark.asyncio
async def test_run_executor_all_tasks():
    executor = RequestAsyncExecutor()

    responses = await executor.run(get_test_task)

    assert responses == [
        Response(200, {"time": 300}), Response(200, {"time": 300})
    ]


@pytest.mark.asyncio
async def test_run_executor_first_task():
    executor = RequestAsyncExecutor(first=True)

    responses = await executor.run(get_test_task)

    assert responses == [Response(200, {"time": 300})]


@pytest.mark.asyncio
async def test_run_executor_first_task_if_tie():
    executor = RequestAsyncExecutor(first=True)

    responses = await executor.run(get_test_task_tie)

    assert responses == [Response(200, {"time": 300})]

