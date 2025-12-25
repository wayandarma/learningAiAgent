import pytest
from unittest.mock import Mock, patch, MagicMock
from src.tools.weather_tool import WeatherTool


@pytest.fixture
def weather_tool():
    """Fixture to create a WeatherTool instance"""
    return WeatherTool()


@pytest.fixture
def mock_point_data():
    """Mock response for points endpoint"""
    return {
        "properties": {
            "relativeLocation": {
                "properties": {
                    "city": "Linn",
                    "state": "KS"
                }
            },
            "forecast": "https://api.weather.gov/gridpoints/TOP/32,81/forecast"
        }
    }


@pytest.fixture
def mock_forecast_data():
    """Mock response for forecast endpoint"""
    return {
        "properties": {
            "periods": [
                {
                    "name": "Tonight",
                    "temperature": 32,
                    "temperatureUnit": "F",
                    "shortForecast": "Partly Cloudy",
                    "detailedForecast": "Partly cloudy, with a low around 32."
                },
                {
                    "name": "Tomorrow",
                    "temperature": 48,
                    "temperatureUnit": "F",
                    "shortForecast": "Sunny",
                    "detailedForecast": "Sunny, with a high near 48."
                }
            ]
        }
    }


def test_weather_tool_initialization(weather_tool):
    """Test that WeatherTool initializes correctly"""
    assert weather_tool.name == "get_weather_forecast"
    assert "United States" in weather_tool.description
    assert weather_tool.client is not None


@patch('src.tools.weather_tool.ApiClient')
def test_weather_tool_run_success(mock_api_client_class, weather_tool, mock_point_data, mock_forecast_data):
    """Test successful weather data fetch"""
    # Setup mock
    mock_client = MagicMock()
    mock_client.base_url = "https://api.weather.gov"
    mock_client.get.side_effect = [mock_point_data, mock_forecast_data]
    weather_tool.client = mock_client
    
    # Execute
    result = weather_tool._run(latitude=39.7456, longitude=-97.0892)
    
    # Verify
    assert "Linn, KS" in result
    assert "Tonight" in result
    assert "32°F" in result
    assert "Partly Cloudy" in result
    assert mock_client.get.call_count == 2


@patch('src.tools.weather_tool.ApiClient')
def test_weather_tool_run_error_handling(mock_api_client_class, weather_tool):
    """Test error handling in weather tool"""
    # Setup mock to raise exception
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("API Error")
    weather_tool.client = mock_client
    
    # Execute
    result = weather_tool._run(latitude=39.7456, longitude=-97.0892)
    
    # Verify error message
    assert "Error fetching weather data" in result
    assert "API Error" in result
