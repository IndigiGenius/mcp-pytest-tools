"""Custom exceptions for mcp-pytest-tools.

This module defines a hierarchy of exceptions used throughout the MCP pytest tools
to provide clear error handling and user-friendly error messages.
"""

from typing import Any


class McpPytestError(Exception):
    """Base exception for all mcp-pytest-tools errors.

    This is the root exception that all other custom exceptions inherit from.
    It provides a common interface for error handling across the application.
    """

    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Initialize the exception with a message and optional context.

        Args:
            message: Human-readable error message
            context: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        return self.message


class TestDiscoveryError(McpPytestError):
    """Exception raised when test discovery fails.

    This exception is raised when pytest fails to discover tests,
    either due to invalid paths, syntax errors, or other collection issues.
    """

    pass


class TestExecutionError(McpPytestError):
    """Exception raised when test execution fails unexpectedly.

    This exception is raised when pytest execution fails due to
    infrastructure issues, not test failures. Test failures are normal
    and are captured in the test results.
    """

    pass


class TestTimeoutError(TestExecutionError):
    """Exception raised when test execution times out.

    This exception is raised when test execution exceeds the specified
    timeout limit.
    """

    pass


class ConfigurationError(McpPytestError):
    """Exception raised when configuration is invalid.

    This exception is raised when pytest configuration files are
    invalid or when tool parameters are misconfigured.
    """

    pass


class PytestNotFoundError(McpPytestError):
    """Exception raised when pytest executable is not found.

    This exception is raised when the pytest command cannot be located
    in the system PATH or virtual environment.
    """

    pass


class InvalidPathError(McpPytestError):
    """Exception raised when a provided path is invalid.

    This exception is raised when test paths don't exist or are not
    accessible for reading.
    """

    pass


class OutputParsingError(McpPytestError):
    """Exception raised when pytest output cannot be parsed.

    This exception is raised when the output from pytest commands
    cannot be parsed into structured data.
    """

    pass
