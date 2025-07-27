# Phase 1, PR 1.1: Project Setup Implementation Example

This document shows the exact implementation for the first PR, demonstrating how to stay within the ~400 line limit while delivering a working MCP server foundation.

## File Structure (Total: ~350 lines)

### 1. pyproject.toml (50 lines)
```toml
[project]
name = "mcp-pytest-tools"
version = "0.1.0"
description = "MCP server providing pytest tools for AI assistants"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "mcp>=0.1.0",
    "pytest>=7.0.0",
    "pydantic>=2.0.0",
    "asyncio",
]

[project.optional-dependencies]
dev = [
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py39"
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["mcp_pytest_tools"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
]
```

### 2. mcp_pytest_tools/__init__.py (10 lines)
```python
"""MCP server providing pytest tools for AI assistants."""

__version__ = "0.1.0"

from .server import PytestMCPServer

__all__ = ["PytestMCPServer", "__version__"]
```

### 3. mcp_pytest_tools/server.py (150 lines)
```python
"""Core MCP server implementation for pytest tools."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp import Server
from mcp.types import Tool, ToolResult
from pydantic import BaseModel, Field

from .models import HealthCheckResponse, ServerConfig

logger = logging.getLogger(__name__)


class PytestMCPServer:
    """MCP server providing pytest functionality to AI assistants."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize the pytest MCP server.
        
        Args:
            config: Optional server configuration
        """
        self.config = config or ServerConfig()
        self.server = Server(name="pytest-tools")
        self._setup_handlers()
        self._tools: Dict[str, Tool] = {}
        self._register_base_tools()
    
    def _setup_handlers(self) -> None:
        """Set up MCP protocol handlers."""
        self.server.add_handler("tools/list", self._handle_list_tools)
        self.server.add_handler("tools/call", self._handle_call_tool)
        self.server.add_handler("health", self._handle_health_check)
    
    def _register_base_tools(self) -> None:
        """Register basic tools available in this phase."""
        # Health check tool for testing
        health_tool = Tool(
            name="health_check",
            description="Check if the pytest MCP server is running",
            inputSchema={
                "type": "object",
                "properties": {
                    "echo": {
                        "type": "string",
                        "description": "Optional message to echo back"
                    }
                },
                "required": []
            }
        )
        self._tools[health_tool.name] = health_tool
    
    async def _handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool listing requests.
        
        Args:
            request: The MCP request
            
        Returns:
            Dictionary containing available tools
        """
        return {
            "tools": list(self._tools.values())
        }
    
    async def _handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution requests.
        
        Args:
            request: The MCP request containing tool name and arguments
            
        Returns:
            Tool execution result
        """
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})
        
        if tool_name not in self._tools:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
        
        # Route to appropriate handler
        if tool_name == "health_check":
            result = await self._health_check(arguments)
        else:
            result = ToolResult(
                error=f"Tool {tool_name} not implemented"
            )
        
        return {"result": result.model_dump()}
    
    async def _health_check(self, arguments: Dict[str, Any]) -> ToolResult:
        """Perform health check.
        
        Args:
            arguments: Tool arguments
            
        Returns:
            Health check result
        """
        echo_msg = arguments.get("echo", "Server is healthy")
        response = HealthCheckResponse(
            status="healthy",
            version="0.1.0",
            message=echo_msg
        )
        
        return ToolResult(
            content=response.model_dump_json(indent=2)
        )
    
    async def _handle_health_check(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle direct health check requests.
        
        Args:
            request: The health check request
            
        Returns:
            Health status
        """
        return {
            "status": "healthy",
            "version": "0.1.0",
            "tools_count": len(self._tools)
        }
    
    async def start(self) -> None:
        """Start the MCP server."""
        logger.info(f"Starting pytest MCP server on {self.config.host}:{self.config.port}")
        await self.server.start(
            host=self.config.host,
            port=self.config.port
        )
    
    async def stop(self) -> None:
        """Stop the MCP server."""
        logger.info("Stopping pytest MCP server")
        await self.server.stop()
```

### 4. mcp_pytest_tools/models.py (80 lines)
```python
"""Pydantic models for request/response validation."""

from typing import Optional
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """Configuration for the MCP server."""
    
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8080, description="Server port")
    max_workers: int = Field(default=4, description="Maximum concurrent workers")
    timeout: int = Field(default=300, description="Default timeout in seconds")
    debug: bool = Field(default=False, description="Enable debug logging")


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(description="Server health status")
    version: str = Field(description="Server version")
    message: Optional[str] = Field(default=None, description="Optional message")


class TestIdentifier(BaseModel):
    """Model for identifying a specific test."""
    
    module: str = Field(description="Test module path")
    class_name: Optional[str] = Field(default=None, description="Test class name")
    function_name: str = Field(description="Test function name")
    
    @property
    def node_id(self) -> str:
        """Get pytest node ID for this test."""
        parts = [self.module]
        if self.class_name:
            parts.append(self.class_name)
        parts.append(self.function_name)
        return "::".join(parts)


class BaseToolRequest(BaseModel):
    """Base model for tool requests."""
    
    timeout: Optional[int] = Field(
        default=None,
        description="Timeout in seconds for this operation"
    )


class BaseToolResponse(BaseModel):
    """Base model for tool responses."""
    
    success: bool = Field(description="Whether the operation succeeded")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    duration: Optional[float] = Field(
        default=None,
        description="Execution time in seconds"
    )
```

### 5. tests/test_server.py (60 lines)
```python
"""Tests for the MCP server."""

import pytest
from mcp.types import ToolResult

from mcp_pytest_tools import PytestMCPServer
from mcp_pytest_tools.models import ServerConfig


@pytest.fixture
async def server():
    """Create a test server instance."""
    config = ServerConfig(port=8081, debug=True)
    server = PytestMCPServer(config)
    yield server


class TestPytestMCPServer:
    """Test the core MCP server functionality."""
    
    async def test_server_initialization(self, server):
        """Test server initializes correctly."""
        assert server.config.port == 8081
        assert server.config.debug is True
        assert len(server._tools) > 0
    
    async def test_list_tools(self, server):
        """Test tool listing."""
        request = {"method": "tools/list"}
        response = await server._handle_list_tools(request)
        
        assert "tools" in response
        assert len(response["tools"]) >= 1
        assert any(tool["name"] == "health_check" for tool in response["tools"])
    
    async def test_health_check_tool(self, server):
        """Test the health check tool."""
        request = {
            "params": {
                "name": "health_check",
                "arguments": {"echo": "test message"}
            }
        }
        response = await server._handle_call_tool(request)
        
        assert "result" in response
        assert "error" not in response["result"]
        assert "test message" in response["result"]["content"]
    
    async def test_unknown_tool(self, server):
        """Test calling an unknown tool."""
        request = {
            "params": {
                "name": "unknown_tool",
                "arguments": {}
            }
        }
        response = await server._handle_call_tool(request)
        
        assert "error" in response
        assert "Unknown tool" in response["error"]["message"]
```

## Summary

This first PR delivers:
- ✅ Working MCP server with health check
- ✅ Pydantic models for type safety
- ✅ Test infrastructure
- ✅ Project configuration
- ✅ Basic error handling

**Total Lines**: ~350 (well within 400-line limit)
**Next PR**: Will add the `list_tests` tool building on this foundation

## Key Design Decisions

1. **Minimal but Complete**: The server works end-to-end with a simple health check
2. **Type Safety**: Pydantic models establish the pattern for all future tools
3. **Testable**: Includes tests that demonstrate the testing approach
4. **Extensible**: Clear structure for adding new tools in subsequent PRs

This approach ensures each PR is reviewable, testable, and delivers value while staying within the line limit.