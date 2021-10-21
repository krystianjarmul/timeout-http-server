from asynctest import patch
from fastapi.testclient import TestClient

from src.entrypoints.api import app

client = TestClient(app)


@patch("src.entrypoints.api.publish")
def test_api_all_success(publish_mock):
    with patch(
            "src.entrypoints.api.get_response",
            return_value=[{"time": 231}, {"time": 123}]
    ):
        response = client.get("/api/all/?timeout=1000")

        assert response.status_code == 200
        assert response.json() == [{"time": 231}, {"time": 123}]


@patch("src.entrypoints.api.publish")
def test_api_all_failed(publish_mock):
    with patch(
            "src.entrypoints.api.get_response",
            return_value={}
    ):
        response = client.get("/api/all/?timeout=1")

        assert response.status_code == 408
        assert response.json() == {"detail": "error - timeout"}


@patch("src.entrypoints.api.publish")
def test_api_first_success(publish_mock):
    with patch(
            "src.entrypoints.api.get_response",
            return_value=[{"time": 123}]
    ):
        response = client.get("/api/first/?timeout=1000")

        assert response.status_code == 200
        assert response.json() == {"time": 123}


@patch("src.entrypoints.api.publish")
def test_api_first_failed(publish_mock):
    with patch(
            "src.entrypoints.api.get_response",
            return_value={}
    ):
        response = client.get("/api/first/?timeout=1")

        assert response.status_code == 408
        assert response.json() == {"detail": "error - timeout"}
