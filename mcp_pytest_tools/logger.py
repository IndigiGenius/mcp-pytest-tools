"""Structured logging system for mcp-pytest-tools.

This module provides structured logging capabilities with context support
and JSON formatting for better observability and debugging.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional


class StructuredLogger:
    """A logger that supports structured logging with context.
    
    This logger wraps the standard Python logging module to provide
    structured logging capabilities with context information.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the structured logger.
        
        Args:
            name: The name of the logger
        """
        self.name = name
        self.logger = logging.getLogger(name)
    
    def _log_with_context(
        self, 
        level: int, 
        message: str, 
        context: Optional[dict[str, Any]] = None
    ) -> None:
        """Log a message with optional context.
        
        Args:
            level: The logging level
            message: The log message
            context: Optional context dictionary
        """
        # Create a custom log record with context
        record = self.logger.makeRecord(
            name=self.name,
            level=level,
            fn="",
            lno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        record.context = context or {}
        
        self.logger.handle(record)
    
    def debug(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        """Log a debug message with optional context."""
        self._log_with_context(logging.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        """Log an info message with optional context."""
        self._log_with_context(logging.INFO, message, context)
    
    def warning(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        """Log a warning message with optional context."""
        self._log_with_context(logging.WARNING, message, context)
    
    def error(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        """Log an error message with optional context."""
        self._log_with_context(logging.ERROR, message, context)
    
    def critical(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        """Log a critical message with optional context."""
        self._log_with_context(logging.CRITICAL, message, context)


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured log output.
    
    This formatter converts log records to JSON format with
    structured fields for better parsing and analysis.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON-formatted log string
        """
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", {})
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(
    level: str = "INFO", 
    json_format: bool = False
) -> None:
    """Set up the logging configuration.
    
    Args:
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Whether to use JSON formatting
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    if json_format:
        # Create a handler with JSON formatting
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        
        logging.basicConfig(
            level=log_level,
            handlers=[handler],
            force=True
        )
    else:
        # Use standard formatting
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            force=True
        )