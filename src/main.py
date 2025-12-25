import sys
from src.client import ApiClient
from src.logger import setup_logger
from src.exceptions import AppError

logger = setup_logger("main")

def main():
    logger.info("Starting Python API Client Application")
    
    # In a real app, you might parse CLI args here
    
    try:
        client = ApiClient()
        logger.info(f"Fetching weather data from: {client.base_url}")
        
        # Testing with a specific point (Kansas)
        endpoint = "points/39.7456,-97.0892"
        data = client.get(endpoint)
        
        import json
        logger.info("Successfully fetched data:")
        print(json.dumps(data, indent=2))
        
    except AppError as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
