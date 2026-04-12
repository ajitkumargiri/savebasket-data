"""
Logging utilities for the scraper.
"""
import logging
import sys
from datetime import datetime


def setup_logger(name, level=logging.INFO):
    """
    Setup and return a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (default: INFO)
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Create formatters and handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


class Logger:
    """Simple logger wrapper for common operations."""
    
    def __init__(self, name):
        self.logger = setup_logger(name)
    
    def info(self, msg):
        """Log info message."""
        self.logger.info(msg)
    
    def debug(self, msg):
        """Log debug message."""
        self.logger.debug(msg)
    
    def warning(self, msg):
        """Log warning message."""
        self.logger.warning(msg)
    
    def error(self, msg):
        """Log error message."""
        self.logger.error(msg)
    
    def success(self, msg):
        """Log success message (using INFO level with prefix)."""
        self.logger.info(f"✅ {msg}")
    
    def start_scraping(self, store_name):
        """Log scraping start."""
        self.info(f"🛒 Starting {store_name} scraper...")
    
    def end_scraping(self, store_name, product_count):
        """Log scraping completion."""
        self.success(f"Scraped {product_count} products from {store_name}")
    
    def progress(self, current, total, message=""):
        """Log progress."""
        pct = (current / total * 100) if total > 0 else 0
        self.info(f"Progress: {current}/{total} ({pct:.1f}%) {message}")
