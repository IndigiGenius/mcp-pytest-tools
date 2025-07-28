"""Tests for MCP server implementation."""

from unittest.mock import patch

import pytest

from mcp_pytest_tools.models import HealthCheckResponse, ServerInfo, ToolInfo
from mcp_pytest_tools.server import MCPPytestServer, create_server, main


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

    def test_get_server_info(self, server):
        """Test structured server info retrieval."""
        info = server.get_server_info()

        assert isinstance(info, ServerInfo)
        assert info.name == "mcp-pytest-tools"
        assert info.version == "0.1.0"
        assert isinstance(info.tools, list)

    def test_register_tool(self, server):
        """Test tool registration functionality."""
        tool_info = ToolInfo(
            name="test_tool",
            description="A test tool",
            parameters={"param1": {"type": "string"}},
        )

        with patch("mcp_pytest_tools.server.logger") as mock_logger:
            server.register_tool("test_tool", tool_info)
            mock_logger.info.assert_called_with("Registered tool: test_tool")

        assert "test_tool" in server.tools
        assert server.tools["test_tool"] == tool_info

    @pytest.mark.asyncio
    async def test_run_method(self, server):
        """Test server run method."""
        with (
            patch.object(server, "startup") as mock_startup,
            patch.object(server, "shutdown") as mock_shutdown,
            patch("mcp_pytest_tools.server.logger") as mock_logger,
        ):
            await server.run()

            mock_startup.assert_called_once()
            mock_shutdown.assert_called_once()
            mock_logger.info.assert_called_with("MCP pytest server running")

    @pytest.mark.asyncio
    async def test_run_method_with_transport_options(self, server):
        """Test server run method with transport options."""
        transport_options = {"host": "localhost", "port": 8080}

        with patch.object(server, "startup"), patch.object(server, "shutdown"):
            await server.run(transport_options)

    @pytest.mark.asyncio
    async def test_handler_registration(self, server):
        """Test that handlers are properly registered."""
        # The handlers are registered during __init__ via _register_handlers
        # This test verifies they exist by checking the server has the _server attribute
        assert hasattr(server, "_server")
        assert server._server is not None


class TestServerFactory:
    """Test suite for server factory functions."""

    def test_create_server(self):
        """Test server factory function."""
        server = create_server()

        assert isinstance(server, MCPPytestServer)
        assert server.name == "mcp-pytest-tools"
        assert server.version == "0.1.0"

    @pytest.mark.asyncio
    async def test_main_function(self):
        """Test main entry point function."""
        with (
            patch("mcp_pytest_tools.server.create_server") as mock_create,
            patch.object(MCPPytestServer, "run") as mock_run,
        ):
            mock_server = MCPPytestServer()
            mock_create.return_value = mock_server

            await main()

            mock_create.assert_called_once()
            mock_run.assert_called_once()
