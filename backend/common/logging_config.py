import logging
import sys
from typing import Optional

class GameLogger:
    """Centralized logging configuration for the game engine."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def setup_logger(cls, name: str = "de_beer_is_los", level: int = logging.INFO) -> logging.Logger:
        """Set up and return the game logger."""
        if cls._logger is not None:
            return cls._logger
        
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(level)
        
        # Avoid duplicate handlers
        if cls._logger.handlers:
            return cls._logger
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        cls._logger.addHandler(console_handler)
        
        return cls._logger
    
    @classmethod
    def get_logger(cls, name: str = "de_beer_is_los") -> logging.Logger:
        """Get the configured logger instance."""
        if cls._logger is None:
            return cls.setup_logger(name)
        return cls._logger

# Initialize the logger
logger = GameLogger.get_logger()