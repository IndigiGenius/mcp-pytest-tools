"""Tests for pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from mcp_pytest_tools.models import (
    ErrorResponse,
    HealthCheckResponse,
    ServerInfo,
    ToolInfo,
)


class TestHealthCheckResponse:
    """Test suite for HealthCheckResponse model."""

    def test_valid_health_check_response(self):
        """Test valid health check response creation."""
        response = HealthCheckResponse(
            status="healthy", server_name="mcp-pytest-tools", version="0.1.0"
        )

        assert response.status == "healthy"
        assert response.server_name == "mcp-pytest-tools"
        assert response.version == "0.1.0"
        assert isinstance(response.timestamp, datetime)

    def test_health_check_response_defaults(self):
        """Test health check response with minimal data."""
        response = HealthCheckResponse(
            status="healthy", server_name="test-server", version="1.0.0"
        )

        assert response.timestamp is not None
        assert isinstance(response.timestamp, datetime)

    def test_invalid_status_validation(self):
        """Test validation fails for invalid status."""
        with pytest.raises(ValidationError):
            HealthCheckResponse(
                status="invalid_status", server_name="test", version="1.0.0"
            )


class TestToolInfo:
    """Test suite for ToolInfo model."""

    def test_valid_tool_info(self):
        """Test valid tool info creation."""
        tool = ToolInfo(
            name="run_test",
            description="Execute a single test",
            parameters={"test_path": {"type": "string", "required": True}},
        )

        assert tool.name == "run_test"
        assert tool.description == "Execute a single test"
        assert "test_path" in tool.parameters

    def test_tool_info_with_empty_parameters(self):
        """Test tool info with empty parameters."""
        tool = ToolInfo(
            name="health_check", description="Server health check", parameters={}
        )

        assert tool.parameters == {}


class TestServerInfo:
    """Test suite for ServerInfo model."""

    def test_valid_server_info(self):
        """Test valid server info creation."""
        info = ServerInfo(
            name="mcp-pytest-tools", version="0.1.0", tools=["run_test", "list_tests"]
        )

        assert info.name == "mcp-pytest-tools"
        assert info.version == "0.1.0"
        assert len(info.tools) == 2
        assert "run_test" in info.tools

    def test_server_info_empty_tools(self):
        """Test server info with empty tools list."""
        info = ServerInfo(name="test-server", version="1.0.0", tools=[])

        assert info.tools == []


class TestErrorResponse:
    """Test suite for ErrorResponse model."""

    def test_valid_error_response(self):
        """Test valid error response creation."""
        error = ErrorResponse(
            error_type="ValidationError",
            message="Invalid test path provided",
            details={"path": "/invalid/path"},
        )

        assert error.error_type == "ValidationError"
        assert error.message == "Invalid test path provided"
        assert error.details["path"] == "/invalid/path"

    def test_error_response_without_details(self):
        """Test error response without details."""
        error = ErrorResponse(
            error_type="RuntimeError", message="Server error occurred"
        )

        assert error.details is None
