"""Tests for test discovery functionality."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from mcp_pytest_tools.tools.discovery import TestDiscoveryTool


class TestTestDiscoveryTool:
    """Test suite for TestDiscoveryTool."""

    @pytest.fixture
    def discovery_tool(self):
        """Create a TestDiscoveryTool instance for testing."""
        return TestDiscoveryTool()

    def test_tool_initialization(self, discovery_tool):
        """Test tool initializes with correct metadata."""
        assert discovery_tool.name == "list_tests"
        assert "Discover and list tests" in discovery_tool.description
        assert isinstance(discovery_tool.parameters, dict)

    def test_tool_parameters_schema(self, discovery_tool):
        """Test tool parameter schema is properly defined."""
        params = discovery_tool.parameters
        
        # Check required path parameter
        assert "path" in params
        assert params["path"]["type"] == "string"
        assert params["path"]["description"]
        
        # Check optional pattern parameter
        assert "pattern" in params  
        assert params["pattern"]["type"] == "string"
        assert not params["pattern"].get("required", True)
        
        # Check optional markers parameter
        assert "markers" in params
        assert params["markers"]["type"] == "string"
        assert not params["markers"].get("required", True)

    @pytest.mark.asyncio
    async def test_discover_tests_basic(self, discovery_tool):
        """Test basic test discovery functionality."""
        test_path = "tests/"
        
        with patch.object(discovery_tool, '_collect_tests') as mock_collect:
            mock_collect.return_value = [
                {
                    "id": "tests/test_example.py::test_function",
                    "path": "tests/test_example.py",
                    "name": "test_function",
                    "module": "tests.test_example",
                    "class": None,
                    "markers": []
                }
            ]
            
            result = await discovery_tool.discover_tests(test_path)
            
            assert isinstance(result, dict)
            assert "tests" in result
            assert "summary" in result
            assert len(result["tests"]) == 1
            mock_collect.assert_called_once_with(test_path, None, None)

    @pytest.mark.asyncio
    async def test_discover_tests_with_pattern(self, discovery_tool):
        """Test test discovery with pattern filtering."""
        test_path = "tests/"
        pattern = "test_specific"
        
        with patch.object(discovery_tool, '_collect_tests') as mock_collect:
            mock_collect.return_value = []
            
            await discovery_tool.discover_tests(test_path, pattern=pattern)
            
            mock_collect.assert_called_once_with(test_path, pattern, None)

    @pytest.mark.asyncio
    async def test_discover_tests_with_markers(self, discovery_tool):
        """Test test discovery with marker filtering."""
        test_path = "tests/"
        markers = "slow"
        
        with patch.object(discovery_tool, '_collect_tests') as mock_collect:
            mock_collect.return_value = []
            
            await discovery_tool.discover_tests(test_path, markers=markers)
            
            mock_collect.assert_called_once_with(test_path, None, markers)

    @pytest.mark.asyncio
    async def test_discover_tests_invalid_path(self, discovery_tool):
        """Test discovery with invalid path raises appropriate error."""
        invalid_path = "/nonexistent/path"
        
        with pytest.raises(ValueError, match="Path does not exist"):
            await discovery_tool.discover_tests(invalid_path)

    @pytest.mark.asyncio
    async def test_collect_tests_subprocess_success(self, discovery_tool):
        """Test successful pytest collection via subprocess."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([
            {
                "nodeid": "tests/test_example.py::test_function",
                "path": "tests/test_example.py", 
                "name": "test_function",
                "module": "tests.test_example",
                "class": None,
                "markers": ["unit"]
            }
        ])
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            result = await discovery_tool._collect_tests("tests/")
            
            assert len(result) == 1
            assert result[0]["id"] == "tests/test_example.py::test_function"

    @pytest.mark.asyncio 
    async def test_collect_tests_subprocess_failure(self, discovery_tool):
        """Test pytest collection failure handling."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Collection error: invalid syntax"
        
        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(RuntimeError, match="Failed to collect tests"):
                await discovery_tool._collect_tests("tests/")

    @pytest.mark.asyncio
    async def test_collect_tests_with_pattern_args(self, discovery_tool):
        """Test that pattern arguments are passed to pytest correctly."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "[]"
            mock_run.return_value.stderr = ""
            
            await discovery_tool._collect_tests("tests/", pattern="test_specific")
            
            # Check that pattern was included in subprocess args
            args = mock_run.call_args[0][0]
            assert "-k" in args
            assert "test_specific" in args

    @pytest.mark.asyncio
    async def test_collect_tests_with_marker_args(self, discovery_tool):
        """Test that marker arguments are passed to pytest correctly."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "[]"
            mock_run.return_value.stderr = ""
            
            await discovery_tool._collect_tests("tests/", markers="slow")
            
            # Check that markers were included in subprocess args
            args = mock_run.call_args[0][0]
            assert "-m" in args
            assert "slow" in args

    def test_format_test_hierarchy(self, discovery_tool):
        """Test hierarchical formatting of test results."""
        tests = [
            {
                "id": "tests/test_models.py::TestUser::test_creation",
                "path": "tests/test_models.py",
                "name": "test_creation", 
                "module": "tests.test_models",
                "class": "TestUser",
                "markers": ["unit"]
            },
            {
                "id": "tests/test_models.py::TestUser::test_validation",
                "path": "tests/test_models.py",
                "name": "test_validation",
                "module": "tests.test_models", 
                "class": "TestUser",
                "markers": ["unit"]
            },
            {
                "id": "tests/test_server.py::test_startup",
                "path": "tests/test_server.py",
                "name": "test_startup",
                "module": "tests.test_server",
                "class": None,
                "markers": ["integration"]
            }
        ]
        
        result = discovery_tool._format_hierarchy(tests)
        
        assert "tests/test_models.py" in result
        assert "tests/test_server.py" in result
        
        models_tests = result["tests/test_models.py"]
        assert "TestUser" in models_tests["classes"]
        assert len(models_tests["classes"]["TestUser"]["tests"]) == 2
        
        server_tests = result["tests/test_server.py"]
        assert len(server_tests["functions"]) == 1

    def test_generate_summary(self, discovery_tool):
        """Test summary generation from test list."""
        tests = [
            {"markers": ["unit"]},
            {"markers": ["integration"]}, 
            {"markers": ["unit", "slow"]},
            {"markers": []}
        ]
        
        summary = discovery_tool._generate_summary(tests)
        
        assert summary["total"] == 4
        assert summary["by_marker"]["unit"] == 2
        assert summary["by_marker"]["integration"] == 1
        assert summary["by_marker"]["slow"] == 1
        assert summary["files"] == set()  # Empty since no file info provided