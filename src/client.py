import httpx
from typing import Any, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.config import settings
from src.logger import setup_logger
from src.exceptions import APIError, APIConnectionError, APITimeoutError

logger = setup_logger(__name__)

class ApiClient:
    def __init__(self, base_url: str = settings.API_BASE_URL, api_key: Optional[str] = settings.API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "WeatherAgent/1.0 (learning_ai_agent)"
        }
        if self.api_key:
             self.headers["Authorization"] = f"Bearer {self.api_key}"
        self.timeout = settings.API_TIMEOUT

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.ConnectError, httpx.TimeoutException, APIConnectionError))
    )
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a GET request with retries
        """
        url =f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"Making GET request to {url}")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=self.headers, params=params)
                self._handle_response(response)
                return response.json()
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise APIConnectionError(f"Failed to connect to {url}") from e
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")
            raise APITimeoutError(f"Request to {url} timed out") from e
        except httpx.HTTPStatusError as e:
             # Caught by _handle_response usually, but good fallback
            logger.error(f"HTTP error: {e}")
            raise APIError(f"HTTP error occurred: {e}", status_code=e.response.status_code) from e
        except Exception as e:
            logger.exception(f"Unexpected error during GET request: {e}")
            raise APIError(f"Unexpected error: {str(e)}") from e

    def _handle_response(self, response: httpx.Response) -> None:
        """
        Handle API response and raise exceptions for error status codes
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"Request failed with status {response.status_code}: {response.text}")
            raise APIError(
                message=f"API Request failed: {response.status_code}",
                status_code=response.status_code,
                details={"response_text": response.text}
            ) from e
