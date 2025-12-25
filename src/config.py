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
    
    # OpenRouter LLM Configuration
    OPENROUTER_API_KEY: Optional[str] = Field(None, description="OpenRouter API Key")
    OPENROUTER_BASE_URL: str = Field("https://openrouter.ai/api/v1", description="OpenRouter base URL")
    LLM_MODEL: str = Field("openai/gpt-4-turbo", description="LLM model to use")
    LLM_TEMPERATURE: float = Field(0.0, description="LLM temperature for responses")
    LLM_MAX_TOKENS: int = Field(1000, description="Maximum tokens for LLM responses")
    
    # App Config
    DEBUG: bool = Field(False, description="Enable debug mode")

settings = Settings()
