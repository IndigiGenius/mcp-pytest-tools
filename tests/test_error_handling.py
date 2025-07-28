"""Tests for error handling functionality in mcp-pytest-tools."""

import pytest
from mcp_pytest_tools.exceptions import (
    McpPytestError,
    TestDiscoveryError,
    TestExecutionError,
    TestTimeoutError,
    ConfigurationError,
    PytestNotFoundError,
    InvalidPathError,
    OutputParsingError,
)


class TestMcpPytestError:
    """Test the base exception class."""
    
    def test_basic_exception_creation(self):
        """Test creating a basic exception with just a message."""
        error = McpPytestError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.context == {}
    
    def test_exception_with_context(self):
        """Test creating an exception with additional context."""
        context = {"test_path": "/path/to/test", "exit_code": 2}
        error = McpPytestError("Test failed", context=context)
        assert str(error) == "Test failed"
        assert error.message == "Test failed"
        assert error.context == context
    
    def test_exception_inheritance(self):
        """Test that McpPytestError inherits from Exception."""
        error = McpPytestError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, McpPytestError)


class TestSpecificExceptions:
    """Test specific exception types."""
    
    def test_test_discovery_error(self):
        """Test TestDiscoveryError creation and inheritance."""
        error = TestDiscoveryError("Discovery failed")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, TestDiscoveryError)
        assert str(error) == "Discovery failed"
    
    def test_test_execution_error(self):
        """Test TestExecutionError creation and inheritance."""
        error = TestExecutionError("Execution failed")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, TestExecutionError)
        assert str(error) == "Execution failed"
    
    def test_test_timeout_error(self):
        """Test TestTimeoutError creation and inheritance."""
        error = TestTimeoutError("Test timed out")
        assert isinstance(error, TestExecutionError)
        assert isinstance(error, TestTimeoutError)
        assert str(error) == "Test timed out"
    
    def test_configuration_error(self):
        """Test ConfigurationError creation and inheritance."""
        error = ConfigurationError("Invalid config")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, ConfigurationError)
        assert str(error) == "Invalid config"
    
    def test_pytest_not_found_error(self):
        """Test PytestNotFoundError creation and inheritance."""
        error = PytestNotFoundError("pytest not found")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, PytestNotFoundError)
        assert str(error) == "pytest not found"
    
    def test_invalid_path_error(self):
        """Test InvalidPathError creation and inheritance."""
        error = InvalidPathError("Path does not exist")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, InvalidPathError)
        assert str(error) == "Path does not exist"
    
    def test_output_parsing_error(self):
        """Test OutputParsingError creation and inheritance."""
        error = OutputParsingError("Could not parse output")
        assert isinstance(error, McpPytestError)
        assert isinstance(error, OutputParsingError)
        assert str(error) == "Could not parse output"


class TestExceptionContext:
    """Test exception context handling."""
    
    def test_context_preservation(self):
        """Test that context is preserved across exception handling."""
        context = {
            "command": ["pytest", "test_file.py"],
            "cwd": "/workspace",
            "timeout": 30
        }
        error = TestExecutionError("Command failed", context=context)
        
        # Simulate exception being raised and caught
        try:
            raise error
        except McpPytestError as caught:
            assert caught.context == context
            assert caught.context["command"] == ["pytest", "test_file.py"]
    
    def test_empty_context_default(self):
        """Test that empty context defaults to empty dict."""
        error = TestDiscoveryError("Test message")
        assert error.context == {}
        assert isinstance(error.context, dict)
    
    def test_none_context_becomes_empty_dict(self):
        """Test that None context becomes empty dict."""
        error = TestDiscoveryError("Test message", context=None)
        assert error.context == {}
        assert isinstance(error.context, dict)


class TestExceptionChaining:
    """Test exception chaining scenarios."""
    
    def test_exception_from_subprocess_error(self):
        """Test creating our exceptions from subprocess errors."""
        import subprocess
        
        # Simulate a subprocess.CalledProcessError
        try:
            raise subprocess.CalledProcessError(1, "pytest", "Error output")
        except subprocess.CalledProcessError as e:
            context = {
                "command": e.cmd,
                "exit_code": e.returncode,
                "output": e.output
            }
            our_error = TestExecutionError(f"Pytest execution failed: {e}", context=context)
            
            assert "Pytest execution failed" in str(our_error)
            assert our_error.context["exit_code"] == 1
            assert our_error.context["command"] == "pytest"
    
    def test_exception_from_file_not_found(self):
        """Test creating our exceptions from FileNotFoundError."""
        try:
            raise FileNotFoundError("No such file or directory: 'nonexistent.py'")
        except FileNotFoundError as e:
            context = {"original_error": str(e)}
            our_error = InvalidPathError(f"Test path not found: {e}", context=context)
            
            assert "Test path not found" in str(our_error)
            assert "nonexistent.py" in our_error.context["original_error"]