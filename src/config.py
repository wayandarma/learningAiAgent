from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True
    )

    API_BASE_URL: str = Field(..., description="Base URL for the API")
    API_KEY: Optional[str] = Field(None, description="API Key for authentication")
    API_TIMEOUT: int = Field(30, description="Default timeout in seconds")
    
    LOG_LEVEL: str = Field("INFO", description="Logging level")

settings = Settings()
