"""Pydantic models for MCP pytest tools."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Health status of the server")
    server_name: str = Field(..., description="Name of the MCP server")
    version: str = Field(..., description="Version of the server")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status field values."""
        allowed_statuses = {"healthy", "unhealthy", "degraded"}
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v


class ToolInfo(BaseModel):
    """Information about an available MCP tool."""

    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Tool parameter schema"
    )


class ServerInfo(BaseModel):
    """Information about the MCP server."""

    name: str = Field(..., description="Server name")
    version: str = Field(..., description="Server version")
    tools: list[str] = Field(
        default_factory=list, description="List of available tool names"
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error_type: str = Field(..., description="Type of error that occurred")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(None, description="Additional error details")


class TestResult(BaseModel):
    """Result of a single test execution."""

    test_id: str = Field(..., description="Unique identifier for the test")
    test_path: str = Field(..., description="Path to the test file")
    test_name: str = Field(..., description="Name of the test function")
    status: str = Field(..., description="Test result status")
    duration: float = Field(..., description="Test execution time in seconds")
    error_message: str | None = Field(None, description="Error message if test failed")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate test status values."""
        allowed_statuses = {"passed", "failed", "skipped", "error"}
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v


class TestSummary(BaseModel):
    """Summary of test execution results."""

    total_tests: int = Field(..., description="Total number of tests")
    passed: int = Field(..., description="Number of passed tests")
    failed: int = Field(..., description="Number of failed tests")
    skipped: int = Field(..., description="Number of skipped tests")
    errors: int = Field(..., description="Number of tests with errors")
    duration: float = Field(..., description="Total execution time in seconds")

    @property
    def success_rate(self) -> float:
        """Calculate test success rate as percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed / self.total_tests) * 100.0


class TestExecutionRequest(BaseModel):
    """Request model for test execution."""

    test_path: str = Field(
        ...,
        description="Path to the test to execute (file::test or file)",
        min_length=1,
    )
    timeout: int = Field(
        30, description="Timeout in seconds for test execution", ge=1, le=3600
    )
    capture_output: bool = Field(
        True, description="Whether to capture stdout and stderr"
    )
    pytest_args: list[str] = Field(
        default_factory=list, description="Additional pytest command line arguments"
    )


class TestExecutionResult(BaseModel):
    """Result of a test execution."""

    test_path: str = Field(..., description="Path to the test that was executed")
    status: str = Field(..., description="Execution status")
    exit_code: int = Field(..., description="Process exit code")
    stdout: str = Field("", description="Captured standard output")
    stderr: str = Field("", description="Captured standard error")
    duration: float = Field(..., description="Execution duration in seconds")
    started_at: datetime = Field(..., description="When execution started")
    completed_at: datetime = Field(..., description="When execution completed")
    error_message: str | None = Field(
        None, description="Error message if execution failed"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate execution status values."""
        allowed_statuses = {"passed", "failed", "error", "timeout", "skipped"}
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v
