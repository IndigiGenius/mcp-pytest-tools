"""Base tool class for mcp-pytest-tools.

This module provides the base class that all MCP pytest tools inherit from,
providing common functionality for logging, error handling, and validation.
"""

import os
import time
from abc import ABC, abstractmethod
from typing import Any

from ..exceptions import InvalidPathError, McpPytestError
from ..logger import StructuredLogger


class BaseTool(ABC):
    """Base class for all MCP pytest tools.

    This class provides common functionality including:
    - Structured logging with context
    - Error handling and recovery
    - Parameter validation
    - Path validation
    - Execution timing
    """

    def __init__(self, name: str) -> None:
        """Initialize the base tool.

        Args:
            name: The name of the tool
        """
        self.name = name
        self.logger = StructuredLogger(f"mcp_pytest_tools.tools.{name}")

    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with the given parameters.

        This method wraps the actual implementation with logging,
        error handling, and timing.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Tool-specific result

        Raises:
            McpPytestError: If execution fails
        """
        start_time = time.time()

        context = {"tool": self.name, "parameters": kwargs}

        self.logger.info("Starting execution", context=context)

        try:
            result = await self._execute(**kwargs)

            duration_ms = (time.time() - start_time) * 1000
            completion_context = {"tool": self.name, "duration_ms": duration_ms}

            self.logger.info("Execution completed", context=completion_context)
            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_context = {
                "tool": self.name,
                "duration_ms": duration_ms,
                "error_type": type(e).__name__,
                "error_message": str(e),
            }

            self.logger.error("Execution failed", context=error_context)

            # Re-raise MCP pytest errors as-is
            if isinstance(e, McpPytestError):
                raise

            # Wrap other exceptions
            raise McpPytestError(f"Tool {self.name} execution failed: {e}") from e

    @abstractmethod
    async def _execute(self, **kwargs: Any) -> Any:
        """Execute the tool's core functionality.

        This method must be implemented by subclasses to provide
        the actual tool functionality.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Tool-specific result
        """
        pass

    def _validate_path(self, path: str) -> None:
        """Validate that a path exists and is accessible.

        Args:
            path: The path to validate

        Raises:
            InvalidPathError: If the path doesn't exist or isn't accessible
        """
        if not os.path.exists(path):
            raise InvalidPathError(
                f"Path does not exist: {path}", context={"path": path}
            )

    def _validate_parameters(
        self, provided: dict[str, Any], required: list[str]
    ) -> None:
        """Validate that all required parameters are provided.

        Args:
            provided: Dictionary of provided parameters
            required: List of required parameter names

        Raises:
            McpPytestError: If required parameters are missing
        """
        missing = [param for param in required if param not in provided]

        if missing:
            raise McpPytestError(
                f"Missing required parameters: {', '.join(missing)}",
                context={
                    "missing_parameters": missing,
                    "provided_parameters": list(provided.keys()),
                    "required_parameters": required,
                },
            )
