"""Tests for MCP server implementation."""

from unittest.mock import patch

import pytest

from mcp_pytest_tools.models import HealthCheckResponse
from mcp_pytest_tools.server import MCPPytestServer


class TestMCPPytestServer:
    """Test suite for MCPPytestServer."""

    @pytest.fixture
    def server(self):
        """Create a server instance for testing."""
        return MCPPytestServer()

    def test_server_initialization(self, server):
        """Test server initializes with correct attributes."""
        assert server.name == "mcp-pytest-tools"
        assert server.version == "0.1.0"
        assert hasattr(server, "tools")
        assert isinstance(server.tools, dict)

    @pytest.mark.asyncio
    async def test_health_check(self, server):
        """Test health check endpoint returns success."""
        response = await server.health_check()

        assert isinstance(response, HealthCheckResponse)
        assert response.status == "healthy"
        assert response.server_name == "mcp-pytest-tools"
        assert response.version == "0.1.0"

    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test tools listing functionality."""
        tools = await server.list_tools()

        assert isinstance(tools, list)
        # Initially empty, will be populated in future PRs
        assert len(tools) == 0

    @pytest.mark.asyncio
    async def test_server_startup(self, server):
        """Test server startup process."""
        with patch("mcp_pytest_tools.server.logger") as mock_logger:
            await server.startup()
            mock_logger.info.assert_called_with("MCP pytest server starting up")

    @pytest.mark.asyncio
    async def test_server_shutdown(self, server):
        """Test server shutdown process."""
        with patch("mcp_pytest_tools.server.logger") as mock_logger:
            await server.shutdown()
            mock_logger.info.assert_called_with("MCP pytest server shutting down")

    def test_server_properties(self, server):
        """Test server property access."""
        assert server.server_info["name"] == "mcp-pytest-tools"
        assert server.server_info["version"] == "0.1.0"
        assert "tools" in server.server_info
