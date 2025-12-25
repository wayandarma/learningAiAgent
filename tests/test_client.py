import pytest
from unittest.mock import Mock, patch
import httpx
from src.client import ApiClient
from src.exceptions import APIError, APIConnectionError

@pytest.fixture
def api_client():
    return ApiClient(base_url="https://test.api.com", api_key="test-key")

def test_init(api_client):
    assert api_client.base_url == "https://test.api.com"
    assert api_client.headers["Authorization"] == "Bearer test-key"

@patch("httpx.Client.get")
def test_get_success(mock_get, api_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response

    response = api_client.get("test-endpoint")
    
    assert response == {"data": "ok"}
    mock_get.assert_called_once()

@patch("httpx.Client.get")
def test_get_retry_on_connection_error(mock_get, api_client):
    # Simulate connection error then success
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    
    mock_get.side_effect = [httpx.ConnectError("Connection failed"), mock_response]

    # The client is configured with tenacity retries, so this should eventually succeed
    # We might need to adjust wait times for tests to run fast, 
    # but for now we trust tenacity's default behavior or mock sleep.
    # However, since we used wait_exponential, this might take a few seconds in real execution.
    # In a real test suite, you'd mock time.sleep.
    
    response = api_client.get("retry-endpoint")
    assert response == {"success": True}
    assert mock_get.call_count == 2
