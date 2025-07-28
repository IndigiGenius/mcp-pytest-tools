"""Tests for test execution functionality."""

import subprocess
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from mcp_pytest_tools.models import TestExecutionRequest, TestExecutionResult
from mcp_pytest_tools.tools.execution import TestExecutionTool


class TestTestExecutionTool:
    """Test suite for TestExecutionTool."""

    @pytest.fixture
    def execution_tool(self):
        """Create a TestExecutionTool instance for testing."""
        return TestExecutionTool()

    def test_tool_initialization(self, execution_tool):
        """Test tool initializes with correct metadata."""
        assert execution_tool.name == "run_test"
        assert "Execute a single test" in execution_tool.description
        assert isinstance(execution_tool.parameters, dict)

    def test_tool_parameters_schema(self, execution_tool):
        """Test tool parameter schema is properly defined."""
        params = execution_tool.parameters

        # Check required test_path parameter
        assert "test_path" in params
        assert params["test_path"]["type"] == "string"
        assert params["test_path"]["required"] is True
        assert params["test_path"]["description"]

        # Check optional timeout parameter
        assert "timeout" in params
        assert params["timeout"]["type"] == "number"
        assert params["timeout"].get("required", False) is False
        assert params["timeout"]["default"] == 30

        # Check optional capture_output parameter
        assert "capture_output" in params
        assert params["capture_output"]["type"] == "boolean"
        assert params["capture_output"]["default"] is True

    @pytest.mark.asyncio
    async def test_execute_test_success(self, execution_tool):
        """Test successful test execution."""
        test_path = "tests/test_example.py::test_function"

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "===== 1 passed in 0.01s ====="
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            result = await execution_tool.execute_test(test_path)

            assert isinstance(result, TestExecutionResult)
            assert result.test_path == test_path
            assert result.status == "passed"
            assert result.exit_code == 0
            assert result.duration > 0
            assert "1 passed" in result.stdout

    @pytest.mark.asyncio
    async def test_execute_test_failure(self, execution_tool):
        """Test failed test execution."""
        test_path = "tests/test_example.py::test_failing"

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "FAILED tests/test_example.py::test_failing"
        mock_result.stderr = "AssertionError: assert 1 == 2"

        with patch("subprocess.run", return_value=mock_result):
            result = await execution_tool.execute_test(test_path)

            assert result.status == "failed"
            assert result.exit_code == 1
            assert "FAILED" in result.stdout
            assert "AssertionError" in result.stderr

    @pytest.mark.asyncio
    async def test_execute_test_with_timeout(self, execution_tool):
        """Test test execution with custom timeout."""
        test_path = "tests/test_slow.py::test_slow_function"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "passed"
            mock_run.return_value.stderr = ""

            await execution_tool.execute_test(test_path, timeout=60)

            # Verify timeout was passed to subprocess.run
            mock_run.assert_called_once()
            assert mock_run.call_args[1]["timeout"] == 60

    @pytest.mark.asyncio
    async def test_execute_test_timeout_exceeded(self, execution_tool):
        """Test handling of test execution timeout."""
        test_path = "tests/test_infinite.py::test_infinite_loop"

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd=["pytest"], timeout=30)

            result = await execution_tool.execute_test(test_path, timeout=30)

            assert result.status == "timeout"
            assert result.exit_code == -1
            assert "timed out after 30 seconds" in result.error_message

    @pytest.mark.asyncio
    async def test_execute_test_not_found(self, execution_tool):
        """Test execution of non-existent test."""
        test_path = "tests/nonexistent.py::test_missing"

        mock_result = Mock()
        mock_result.returncode = 4  # pytest exit code for no tests collected
        mock_result.stdout = "no tests ran"
        mock_result.stderr = "ERROR: not found"

        with patch("subprocess.run", return_value=mock_result):
            result = await execution_tool.execute_test(test_path)

            assert result.status == "error"
            assert result.exit_code == 4
            assert result.error_message is not None

    @pytest.mark.asyncio
    async def test_execute_test_without_output_capture(self, execution_tool):
        """Test execution without capturing output."""
        test_path = "tests/test_example.py::test_function"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = None
            mock_run.return_value.stderr = None

            result = await execution_tool.execute_test(test_path, capture_output=False)

            # Verify capture_output was False in subprocess call
            mock_run.assert_called_once()
            assert mock_run.call_args[1]["capture_output"] is False
            assert result.stdout == ""
            assert result.stderr == ""

    @pytest.mark.asyncio
    async def test_parse_pytest_output(self, execution_tool):
        """Test parsing of pytest output for test details."""
        # Typical pytest output
        output = """
collected 1 item

tests/test_example.py::test_function PASSED                              [100%]

============================== 1 passed in 0.05s ==============================
"""

        with patch.object(
            execution_tool.output_parser, "parse_test_output"
        ) as mock_parse:
            mock_parse.return_value = {
                "passed": 1,
                "failed": 0,
                "duration": 0.05,
                "details": [],
            }

            parsed = execution_tool._parse_output(output, "")

            assert parsed["passed"] == 1
            assert parsed["failed"] == 0
            assert parsed["duration"] == 0.05

    def test_build_pytest_command(self, execution_tool):
        """Test pytest command building with various options."""
        # Basic command
        cmd = execution_tool._build_command("tests/test_example.py::test_func")
        assert cmd == [
            "python",
            "-m",
            "pytest",
            "-v",
            "tests/test_example.py::test_func",
        ]

        # With additional pytest args
        cmd = execution_tool._build_command(
            "tests/test_example.py", pytest_args=["-x", "--tb=short"]
        )
        assert "-x" in cmd
        assert "--tb=short" in cmd

    @pytest.mark.asyncio
    async def test_request_validation(self, execution_tool):
        """Test that execution requests are properly validated."""
        # Valid request
        request = TestExecutionRequest(
            test_path="tests/test_example.py::test_function",
            timeout=60,
            capture_output=True,
        )
        assert request.test_path == "tests/test_example.py::test_function"
        assert request.timeout == 60

        # Invalid request should raise validation error
        with pytest.raises(ValueError):
            TestExecutionRequest(
                test_path="",  # Empty path should fail
                timeout=60,
            )

    @pytest.mark.asyncio
    async def test_result_serialization(self, execution_tool):
        """Test that execution results can be properly serialized."""
        result = TestExecutionResult(
            test_path="tests/test_example.py::test_function",
            status="passed",
            exit_code=0,
            stdout="1 passed",
            stderr="",
            duration=0.05,
            started_at=datetime.now(),
            completed_at=datetime.now(),
        )

        # Should be serializable to dict
        result_dict = result.model_dump()
        assert result_dict["test_path"] == "tests/test_example.py::test_function"
        assert result_dict["status"] == "passed"
        assert isinstance(result_dict["started_at"], datetime)  # Datetime object

        # Check JSON serialization
        result_json = result.model_dump(mode="json")
        assert isinstance(
            result_json["started_at"], str
        )  # Datetime serialized to string
