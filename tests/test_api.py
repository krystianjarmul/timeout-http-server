import asyncio
import pytest
from asynctest import patch
from fastapi.testclient import TestClient

from src.entrypoints.api import app

client = TestClient(app)


def test_api_all_success():
    with patch(
            "src.entrypoints.api.ExponeaHttpTestingClient.get",
            return_value=[{"time": 231}, {"time": 123}]
    ):
        response = client.get("/api/all/?time=1000")

        assert response.status_code == 200
        assert response.json() == [{"time": 231}, {"time": 123}]


def test_api_all_failed():
    with patch(
            "src.entrypoints.api.ExponeaHttpTestingClient.get",
            return_value={}
    ):
        response = client.get("/api/all/?time=1")

        assert response.status_code == 408
        assert response.json() == {"detail": "error - timeout"}


def test_api_first_success():
    with patch(
            "src.entrypoints.api.ExponeaHttpTestingClient.get",
            return_value=[{"time": 123}]
    ):
        response = client.get("/api/first/?time=1000")

        assert response.status_code == 200
        assert response.json() == {"time": 123}


def test_api_first_failed():
    with patch(
            "src.entrypoints.api.ExponeaHttpTestingClient.get",
            return_value={}
    ):
        response = client.get("/api/first/?time=1")

        assert response.status_code == 408
        assert response.json() == {"detail": "error - timeout"}
