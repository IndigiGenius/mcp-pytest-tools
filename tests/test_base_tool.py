"""Tests for base tool functionality in mcp-pytest-tools."""

import pytest

from mcp_pytest_tools.exceptions import (
    InvalidPathError,
    McpPytestError,
    TestExecutionError,
)
from mcp_pytest_tools.tools.base import BaseTool


class MockTool(BaseTool):
    """Mock tool for testing base functionality."""

    def __init__(self, name: str = "mock_tool"):
        super().__init__(name)

    async def _execute(self, **kwargs):
        """Mock implementation of execute method."""
        if kwargs.get("should_fail"):
            raise TestExecutionError("Mock execution failed")
        return {"result": "success", "input": kwargs}


class TestBaseTool:
    """Test the base tool class."""

    def test_tool_creation(self):
        """Test creating a base tool."""
        tool = MockTool("test_tool")
        assert tool.name == "test_tool"
        assert tool.logger is not None
        assert tool.logger.name == "mcp_pytest_tools.tools.test_tool"

    def test_tool_creation_default_name(self):
        """Test creating a tool with default name."""
        tool = MockTool()
        assert tool.name == "mock_tool"

    @pytest.mark.asyncio
    async def test_successful_execution(self):
        """Test successful tool execution."""
        tool = MockTool()
        result = await tool.execute(param1="value1", param2="value2")

        assert result["result"] == "success"
        assert result["input"]["param1"] == "value1"
        assert result["input"]["param2"] == "value2"

    @pytest.mark.asyncio
    async def test_execution_with_logging(self, caplog):
        """Test that execution includes proper logging."""
        import logging

        tool = MockTool("logged_tool")

        with caplog.at_level(logging.INFO):
            await tool.execute(test_param="test_value")

        # Check that execution was logged
        assert any("Starting execution" in record.message for record in caplog.records)
        assert any("Execution completed" in record.message for record in caplog.records)

        # Check that context was logged
        contexts = [getattr(record, "context", {}) for record in caplog.records]
        assert any(ctx.get("tool") == "logged_tool" for ctx in contexts)

    @pytest.mark.asyncio
    async def test_execution_failure_handling(self, caplog):
        """Test that execution failures are properly handled."""
        import logging

        tool = MockTool("failing_tool")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(TestExecutionError) as exc_info:
                await tool.execute(should_fail=True)

        assert "Mock execution failed" in str(exc_info.value)

        # Check that error was logged
        assert any("Execution failed" in record.message for record in caplog.records)
        error_contexts = [
            getattr(record, "context", {})
            for record in caplog.records
            if record.levelname == "ERROR"
        ]
        assert any(ctx.get("tool") == "failing_tool" for ctx in error_contexts)

    @pytest.mark.asyncio
    async def test_execution_timing(self, caplog):
        """Test that execution timing is logged."""
        import logging

        tool = MockTool("timed_tool")

        with caplog.at_level(logging.INFO):
            await tool.execute()

        # Check that completion log includes duration
        completion_records = [
            record
            for record in caplog.records
            if "Execution completed" in record.message
        ]
        assert len(completion_records) == 1
        context = getattr(completion_records[0], "context", {})
        assert "duration_ms" in context
        assert isinstance(context["duration_ms"], int | float)
        assert context["duration_ms"] >= 0


class TestBaseToolValidation:
    """Test base tool validation functionality."""

    def test_validate_path_existing_file(self, tmp_path):
        """Test path validation for existing files."""
        tool = MockTool()
        test_file = tmp_path / "test.py"
        test_file.write_text("# test file")

        # Should not raise an exception
        tool._validate_path(str(test_file))

    def test_validate_path_existing_directory(self, tmp_path):
        """Test path validation for existing directories."""
        tool = MockTool()
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Should not raise an exception
        tool._validate_path(str(test_dir))

    def test_validate_path_nonexistent(self, tmp_path):
        """Test path validation for nonexistent paths."""
        tool = MockTool()
        nonexistent = tmp_path / "nonexistent.py"

        with pytest.raises(InvalidPathError) as exc_info:
            tool._validate_path(str(nonexistent))

        assert "does not exist" in str(exc_info.value)
        assert str(nonexistent) in str(exc_info.value)

    def test_validate_parameters_required(self):
        """Test parameter validation for required parameters."""
        tool = MockTool()

        required = ["param1", "param2"]
        provided = {"param1": "value1", "param2": "value2", "param3": "value3"}

        # Should not raise an exception
        tool._validate_parameters(provided, required)

    def test_validate_parameters_missing(self):
        """Test parameter validation with missing required parameters."""
        tool = MockTool()

        required = ["param1", "param2", "param3"]
        provided = {"param1": "value1", "param2": "value2"}

        with pytest.raises(McpPytestError) as exc_info:
            tool._validate_parameters(provided, required)

        assert "Missing required parameters" in str(exc_info.value)
        assert "param3" in str(exc_info.value)

    def test_validate_parameters_empty_required(self):
        """Test parameter validation with no required parameters."""
        tool = MockTool()

        # Should not raise an exception
        tool._validate_parameters({"any": "params"}, [])
        tool._validate_parameters({}, [])


class TestBaseToolContextManagement:
    """Test context management in base tool."""

    @pytest.mark.asyncio
    async def test_context_includes_tool_info(self, caplog):
        """Test that logging context includes tool information."""
        import logging

        tool = MockTool("context_tool")

        with caplog.at_level(logging.INFO):
            await tool.execute(test_param="test_value")

        # Check that all log records have tool context
        for record in caplog.records:
            context = getattr(record, "context", {})
            assert context.get("tool") == "context_tool"

    @pytest.mark.asyncio
    async def test_context_includes_parameters(self, caplog):
        """Test that logging context includes execution parameters."""
        import logging

        tool = MockTool("param_tool")

        params = {"path": "/test/path", "timeout": 30}

        with caplog.at_level(logging.INFO):
            await tool.execute(**params)

        # Check that start log includes parameters
        start_records = [
            record
            for record in caplog.records
            if "Starting execution" in record.message
        ]
        assert len(start_records) == 1
        context = getattr(start_records[0], "context", {})
        assert context.get("parameters") == params

    @pytest.mark.asyncio
    async def test_error_context_includes_exception_info(self, caplog):
        """Test that error context includes exception information."""
        import logging

        tool = MockTool("error_tool")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(TestExecutionError):
                await tool.execute(should_fail=True)

        # Check error log context
        error_records = [
            record for record in caplog.records if record.levelname == "ERROR"
        ]
        assert len(error_records) == 1
        context = getattr(error_records[0], "context", {})
        assert "error_type" in context
        assert context["error_type"] == "TestExecutionError"
        assert "error_message" in context


class TestBaseToolSubclassRequirements:
    """Test requirements for subclassing BaseTool."""

    def test_abstract_execute_method(self):
        """Test that _execute method must be implemented."""
        # BaseTool should be abstract and require _execute implementation
        with pytest.raises(TypeError):
            # This should fail because _execute is not implemented
            class IncompleteTool(BaseTool):
                pass

            IncompleteTool()  # type: ignore

    @pytest.mark.asyncio
    async def test_execute_calls_internal_execute(self):
        """Test that execute method calls _execute with proper wrapping."""

        class TestTool(BaseTool):
            def __init__(self):
                super().__init__("test_tool")
                self._execute_called = False
                self._execute_args = None
                self._execute_kwargs = None

            async def _execute(self, *args, **kwargs):
                self._execute_called = True
                self._execute_args = args
                self._execute_kwargs = kwargs
                return {"success": True}

        tool = TestTool()
        result = await tool.execute(param1="value1", param2="value2")

        assert tool._execute_called
        assert tool._execute_kwargs == {"param1": "value1", "param2": "value2"}
        assert result == {"success": True}
