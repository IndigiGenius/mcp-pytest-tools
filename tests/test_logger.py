"""Tests for structured logging functionality in mcp-pytest-tools."""

import json
import logging
from unittest.mock import patch

from mcp_pytest_tools.logger import StructuredLogger, setup_logging


class TestStructuredLogger:
    """Test the structured logger class."""

    def test_logger_creation(self):
        """Test creating a structured logger."""
        logger = StructuredLogger("test_logger")
        assert logger.name == "test_logger"
        assert logger.logger.name == "test_logger"

    def test_log_with_context(self, caplog):
        """Test logging with structured context."""
        logger = StructuredLogger("test_logger")
        context = {"test_path": "/path/to/test", "operation": "discovery"}

        with caplog.at_level(logging.INFO):
            logger.info("Test discovery started", context=context)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.message == "Test discovery started"
        assert hasattr(record, "context")
        assert record.context == context

    def test_log_without_context(self, caplog):
        """Test logging without context."""
        logger = StructuredLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Simple message")

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.message == "Simple message"
        assert hasattr(record, "context")
        assert record.context == {}

    def test_all_log_levels(self, caplog):
        """Test all logging levels."""
        logger = StructuredLogger("test_logger")

        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")

        assert len(caplog.records) == 5
        levels = [record.levelname for record in caplog.records]
        assert levels == ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_context_serialization(self, caplog):
        """Test that complex context objects are handled properly."""
        logger = StructuredLogger("test_logger")
        context = {
            "command": ["pytest", "--verbose"],
            "timeout": 30.5,
            "success": True,
            "nested": {"key": "value"},
        }

        with caplog.at_level(logging.INFO):
            logger.info("Complex context", context=context)

        record = caplog.records[0]
        assert record.context == context
        # Ensure it's JSON serializable
        json.dumps(record.context)


class TestJsonFormatter:
    """Test the JSON formatter for structured logging."""

    def test_json_formatting(self):
        """Test that logs are formatted as valid JSON."""
        from mcp_pytest_tools.logger import JsonFormatter

        formatter = JsonFormatter()

        # Create a log record
        record = logging.LogRecord(
            name="test_json",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.context = {"key": "value"}

        formatted = formatter.format(record)
        parsed = json.loads(formatted)

        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message"
        assert parsed["logger"] == "test_json"
        assert parsed["context"] == {"key": "value"}
        assert "timestamp" in parsed

    def test_json_formatting_without_context(self):
        """Test JSON formatting when no context is present."""
        from mcp_pytest_tools.logger import JsonFormatter

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test_json",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error message",
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)
        parsed = json.loads(formatted)

        assert parsed["level"] == "ERROR"
        assert parsed["message"] == "Error message"
        assert parsed["context"] == {}

    def test_json_formatting_with_exception(self):
        """Test JSON formatting with exception information."""
        import sys

        from mcp_pytest_tools.logger import JsonFormatter

        formatter = JsonFormatter()

        try:
            raise ValueError("Test exception")
        except ValueError:
            exc_info = sys.exc_info()
            record = logging.LogRecord(
                name="test_json",
                level=logging.ERROR,
                pathname="test.py",
                lineno=10,
                msg="Exception occurred",
                args=(),
                exc_info=exc_info,
            )
            record.context = {"operation": "test"}

            formatted = formatter.format(record)
            parsed = json.loads(formatted)

            assert parsed["level"] == "ERROR"
            assert parsed["message"] == "Exception occurred"
            assert "exception" in parsed
            assert "ValueError" in parsed["exception"]
            assert "Test exception" in parsed["exception"]


class TestSetupLogging:
    """Test the logging setup function."""

    def test_setup_logging_with_level(self):
        """Test setting up logging with a specific level."""
        with patch("mcp_pytest_tools.logger.logging.basicConfig") as mock_config:
            setup_logging(level="DEBUG")
            mock_config.assert_called_once()
            args, kwargs = mock_config.call_args
            assert kwargs["level"] == logging.DEBUG

    def test_setup_logging_with_json_format(self):
        """Test setting up logging with JSON formatting."""
        with patch("mcp_pytest_tools.logger.logging.basicConfig") as mock_config:
            setup_logging(json_format=True)
            mock_config.assert_called_once()
            args, kwargs = mock_config.call_args
            # Verify that a JsonFormatter was used
            assert "handlers" in kwargs

    def test_setup_logging_defaults(self):
        """Test setup_logging with default parameters."""
        with patch("mcp_pytest_tools.logger.logging.basicConfig") as mock_config:
            setup_logging()
            mock_config.assert_called_once()
            args, kwargs = mock_config.call_args
            assert kwargs["level"] == logging.INFO


class TestLoggingIntegration:
    """Test integration with actual pytest execution scenarios."""

    def test_log_test_discovery(self, caplog):
        """Test logging during test discovery."""
        logger = StructuredLogger("mcp_pytest_tools.discovery")

        context = {"path": "tests/", "pattern": "test_*.py", "collected_count": 15}

        with caplog.at_level(logging.INFO):
            logger.info("Test discovery completed", context=context)

        record = caplog.records[0]
        assert "Test discovery completed" in record.message
        assert record.context["collected_count"] == 15

    def test_log_test_execution(self, caplog):
        """Test logging during test execution."""
        logger = StructuredLogger("mcp_pytest_tools.execution")

        context = {
            "test_path": "tests/test_example.py::TestClass::test_method",
            "timeout": 30,
            "exit_code": 0,
            "duration": 2.5,
        }

        with caplog.at_level(logging.INFO):
            logger.info("Test execution completed", context=context)

        record = caplog.records[0]
        assert record.context["duration"] == 2.5
        assert record.context["exit_code"] == 0

    def test_log_error_with_context(self, caplog):
        """Test error logging with rich context."""
        logger = StructuredLogger("mcp_pytest_tools.error")

        context = {
            "command": ["pytest", "nonexistent.py"],
            "exit_code": 4,
            "stderr": "ERROR: file or directory not found: nonexistent.py",
        }

        with caplog.at_level(logging.ERROR):
            logger.error("Test execution failed", context=context)

        record = caplog.records[0]
        assert record.levelname == "ERROR"
        assert record.context["exit_code"] == 4
        assert "not found" in record.context["stderr"]
