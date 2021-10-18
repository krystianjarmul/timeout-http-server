from unittest.mock import patch, Mock

from external import RequestsClient


url = "https://exponea-engineering-assignment.appspot.com/api/work"


def test_requests_client_get_data_from_external_service_success():
    client = RequestsClient()
    response_mock = Mock(status_code=200, json=lambda: {"time": 300})

    with patch("requests.get", return_value=response_mock):
        response = client.get(url)

    assert response.status_code == 200
    assert response.body == {"time": 300}


def test_requests_client_get_data_failed_internal_server_error():
    client = RequestsClient()
    response_mock = Mock(status_code=500, json=lambda: "Internal server error")

    with patch("requests.get", return_value=response_mock):
        response = client.get(url)

    assert response.status_code == 500
    assert response.body == "Internal server error"


def test_requests_client_get_data_failed_to_many_requests():
    client = RequestsClient()
    response_mock = Mock(status_code=429, json=lambda: "Internal server error")

    with patch("requests.get", return_value=response_mock):
        response = client.get(url)

    assert response.status_code == 429
    assert response.body == "Internal server error"
