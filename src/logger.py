import logging
import sys
from src.config import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance with industry standard formatting
    """
    logger = logging.getLogger(name)
    
    # Check if logger is already configured to prevent duplicate logs
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(settings.LOG_LEVEL)
    
    handler = logging.StreamHandler(sys.stdout)
    
    # In production/default mode, we only want to show WARNINGs and above to console
    # To keep the UI clean
    if settings.DEBUG:
        handler.setLevel(settings.LOG_LEVEL)
    else:
        handler.setLevel(logging.WARNING)
    
    # JSON-like structured format is often preferred in production, 
    # but a readable format is better for development. 
    # Here is a robust human-readable standard format.
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    # Prevent propagation to root logger to avoid double logging if root is configured
    logger.propagate = False
    
    return logger
