from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

from src.client import ApiClient
from src.logger import setup_logger

logger = setup_logger(__name__)


class WeatherInput(BaseModel):
    """Input schema for weather tool"""
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")


class WeatherTool(BaseTool):
    """Tool for fetching weather data from weather.gov API"""
    
    name: str = "get_weather_forecast"
    description: str = """
    Useful for getting weather forecast for a specific location in the United States.
    Input should be latitude and longitude coordinates.
    Returns detailed weather forecast information including temperature, conditions, and alerts.
    Only works for locations within the United States.
    """
    args_schema: Type[BaseModel] = WeatherInput
    
    # Allow extra fields for client
    model_config = {"arbitrary_types_allowed": True, "extra": "allow"}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize client after parent init
        object.__setattr__(self, 'client', ApiClient())
    
    def _run(
        self,
        latitude: float,
        longitude: float,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the tool to fetch weather data"""
        try:
            logger.info(f"Fetching weather for coordinates: {latitude}, {longitude}")
            
            # Step 1: Get grid point data
            endpoint = f"points/{latitude},{longitude}"
            point_data = self.client.get(endpoint)
            
            # Extract location information
            location_props = point_data.get('properties', {})
            relative_location = location_props.get('relativeLocation', {}).get('properties', {})
            city = relative_location.get('city', 'Unknown')
            state = relative_location.get('state', 'Unknown')
            
            # Step 2: Get forecast URL
            forecast_url = location_props.get('forecast')
            if not forecast_url:
                return f"Unable to get forecast URL for coordinates {latitude}, {longitude}"
            
            # Extract endpoint from full URL
            forecast_endpoint = forecast_url.replace(self.client.base_url + "/", "")
            
            # Step 3: Get actual forecast
            forecast_data = self.client.get(forecast_endpoint)
            
            # Format the response
            periods = forecast_data.get('properties', {}).get('periods', [])[:3]  # Get next 3 periods
            
            if not periods:
                return f"No forecast data available for {city}, {state}"
            
            result = f"Weather forecast for {city}, {state}:\n\n"
            
            for period in periods:
                result += f"**{period['name']}**: {period['temperature']}°{period['temperatureUnit']}\n"
                result += f"Conditions: {period['shortForecast']}\n"
                result += f"Details: {period['detailedForecast']}\n\n"
            
            return result.strip()
            
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return f"Error fetching weather data: {str(e)}. Please ensure the coordinates are within the United States."
    
    async def _arun(self, *args, **kwargs):
        """Async version (not implemented)"""
        raise NotImplementedError("Async execution not implemented yet")
