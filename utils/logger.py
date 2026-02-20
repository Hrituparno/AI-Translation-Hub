"""
Centralized logging configuration.
"""

import logging
import sys
from core.config import LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str = None) -> logging.Logger:
    """
    Setup and configure logger.
    
    Args:
        name: Logger name (defaults to root logger)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # Formatter
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


# Initialize root logger
setup_logger()
