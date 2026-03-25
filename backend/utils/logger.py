"""
Logging configuration for the application.

Sets up structured logging with JSON format for production and plain text for development.

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened", extra={"detail": "value"})
"""

import logging
import sys
from config import get_settings

settings = get_settings()


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        
        # Format
        if settings.debug:
            # Development: simple format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            # Production: JSON format (parsed by log aggregators)
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "name": "%(name)s", '
                '"level": "%(levelname)s", "message": "%(message)s"}'
            )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(getattr(logging, settings.log_level))
    return logger
