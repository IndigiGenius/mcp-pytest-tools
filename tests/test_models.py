"""Tests for pydantic models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from mcp_pytest_tools.models import (
    ErrorResponse,
    HealthCheckResponse,
    ServerInfo,
    TestResult,
    TestSummary,
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


class TestTestResult:
    """Test suite for TestResult model."""

    def test_valid_test_result(self):
        """Test valid test result creation."""
        result = TestResult(
            test_id="test_001",
            test_path="tests/test_example.py",
            test_name="test_example_function",
            status="passed",
            duration=0.5,
            error_message=None,
        )

        assert result.test_id == "test_001"
        assert result.test_path == "tests/test_example.py"
        assert result.test_name == "test_example_function"
        assert result.status == "passed"
        assert result.duration == 0.5
        assert result.error_message is None

    def test_failed_test_result_with_error(self):
        """Test failed test result with error message."""
        result = TestResult(
            test_id="test_002",
            test_path="tests/test_failing.py",
            test_name="test_failing_function",
            status="failed",
            duration=0.2,
            error_message="AssertionError: 1 != 2",
        )

        assert result.status == "failed"
        assert result.error_message == "AssertionError: 1 != 2"

    def test_invalid_test_status_validation(self):
        """Test validation fails for invalid test status."""
        with pytest.raises(ValidationError):
            TestResult(
                test_id="test_003",
                test_path="tests/test_invalid.py",
                test_name="test_invalid_function",
                status="invalid_status",
                duration=0.1,
            )


class TestTestSummary:
    """Test suite for TestSummary model."""

    def test_valid_test_summary(self):
        """Test valid test summary creation."""
        summary = TestSummary(
            total_tests=10,
            passed=8,
            failed=1,
            skipped=1,
            errors=0,
            duration=5.5,
        )

        assert summary.total_tests == 10
        assert summary.passed == 8
        assert summary.failed == 1
        assert summary.skipped == 1
        assert summary.errors == 0
        assert summary.duration == 5.5

    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        summary = TestSummary(
            total_tests=10,
            passed=8,
            failed=2,
            skipped=0,
            errors=0,
            duration=3.0,
        )

        assert summary.success_rate == 80.0

    def test_success_rate_with_zero_tests(self):
        """Test success rate calculation with zero tests."""
        summary = TestSummary(
            total_tests=0,
            passed=0,
            failed=0,
            skipped=0,
            errors=0,
            duration=0.0,
        )

        assert summary.success_rate == 0.0
