class AppError(Exception):
    """Base exception for the application"""
    pass

class ConfigurationError(AppError):
    """Raised when there is a configuration error"""
    pass

class APIError(AppError):
    """Base exception for API related errors"""
    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}

class APIConnectionError(APIError):
    """Raised when connection to API fails"""
    pass

class APITimeoutError(APIError):
    """Raised when API request times out"""
    pass
