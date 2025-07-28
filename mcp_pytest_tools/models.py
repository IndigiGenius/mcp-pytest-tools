"""Pydantic models for MCP pytest tools."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Health status of the server")
    server_name: str = Field(..., description="Name of the MCP server")
    version: str = Field(..., description="Version of the server")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Validate status field values."""
        allowed_statuses = {"healthy", "unhealthy", "degraded"}
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v


class ToolInfo(BaseModel):
    """Information about an available MCP tool."""
    
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameter schema")


class ServerInfo(BaseModel):
    """Information about the MCP server."""
    
    name: str = Field(..., description="Server name")
    version: str = Field(..., description="Server version")
    tools: List[str] = Field(default_factory=list, description="List of available tool names")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error_type: str = Field(..., description="Type of error that occurred")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class TestResult(BaseModel):
    """Result of a single test execution."""
    
    test_id: str = Field(..., description="Unique identifier for the test")
    test_path: str = Field(..., description="Path to the test file")
    test_name: str = Field(..., description="Name of the test function")
    status: str = Field(..., description="Test result status")
    duration: float = Field(..., description="Test execution time in seconds")
    error_message: Optional[str] = Field(None, description="Error message if test failed")
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
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