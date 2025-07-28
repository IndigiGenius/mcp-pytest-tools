"""Test discovery tool for finding and listing pytest tests."""

import json
import subprocess
from pathlib import Path
from typing import Any

from mcp_pytest_tools.parsers.collector import PytestCollector


class TestDiscoveryTool:
    """Tool for discovering and listing pytest tests with filtering capabilities."""

    def __init__(self) -> None:
        """Initialize the test discovery tool."""
        self.name = "list_tests"
        self.description = (
            "Discover and list tests in the specified path with optional filtering"
        )
        self.parameters = {
            "path": {
                "type": "string",
                "description": "Path to search for tests (file or directory)",
                "required": True,
            },
            "pattern": {
                "type": "string",
                "description": "Test name pattern to filter tests (pytest -k syntax)",
                "required": False,
            },
            "markers": {
                "type": "string",
                "description": "Test markers to filter by (pytest -m syntax)",
                "required": False,
            },
        }
        self.collector = PytestCollector()

    async def discover_tests(
        self, path: str, pattern: str | None = None, markers: str | None = None
    ) -> dict[str, Any]:
        """
        Discover tests in the specified path with optional filtering.

        Args:
            path: Path to search for tests
            pattern: Optional pattern to filter test names
            markers: Optional markers to filter tests by

        Returns:
            Dictionary containing discovered tests and summary information

        Raises:
            ValueError: If path does not exist
            RuntimeError: If test collection fails
        """
        # Validate path exists
        test_path = Path(path)
        if not test_path.exists():
            raise ValueError(f"Path does not exist: {path}")

        # Collect tests using subprocess call to pytest
        tests = await self._collect_tests(path, pattern, markers)

        # Format results into hierarchical structure
        hierarchy = self._format_hierarchy(tests)

        # Generate summary statistics
        summary = self._generate_summary(tests)

        return {"tests": hierarchy, "summary": summary, "total_count": len(tests)}

    async def _collect_tests(
        self, path: str, pattern: str | None = None, markers: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Run pytest collection to discover tests.

        Args:
            path: Path to collect tests from
            pattern: Optional test name pattern filter
            markers: Optional marker filter

        Returns:
            List of discovered test dictionaries

        Raises:
            RuntimeError: If pytest collection fails
        """
        # Build pytest command
        cmd = [
            "python",
            "-m",
            "pytest",
            "--collect-only",
            "--quiet",
            "--json-report",
            "--json-report-file=/dev/stdout",
            path,
        ]

        # Add pattern filter if specified
        if pattern:
            cmd.extend(["-k", pattern])

        # Add marker filter if specified
        if markers:
            cmd.extend(["-m", markers])

        # Run pytest collection
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired as e:
            raise RuntimeError("Test collection timed out") from e

        if result.returncode != 0:
            error_msg = result.stderr or "Unknown collection error"
            raise RuntimeError(f"Failed to collect tests: {error_msg}")

        # Parse JSON output
        try:
            if result.stdout.strip():
                # Try to parse as JSON first
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, dict) and "tests" in data:
                        tests = data["tests"]
                    elif isinstance(data, list):
                        tests = data
                    else:
                        tests = []
                except json.JSONDecodeError:
                    tests = []
            else:
                tests = []

            # Normalize field names (nodeid -> id)
            for test in tests:
                if "nodeid" in test and "id" not in test:
                    test["id"] = test["nodeid"]

            return tests  # type: ignore[no-any-return]

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse pytest output: {e}") from e

    def _format_hierarchy(self, tests: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Format flat test list into hierarchical structure organized by file.

        Args:
            tests: List of test dictionaries

        Returns:
            Hierarchical dictionary organized by test file
        """
        hierarchy: dict[str, Any] = {}

        for test in tests:
            file_path = test.get("path", "unknown")
            test_class = test.get("class")
            test_name = test.get("name", "")

            # Initialize file entry if not exists
            if file_path not in hierarchy:
                hierarchy[file_path] = {"functions": [], "classes": {}}

            file_entry = hierarchy[file_path]

            if test_class:
                # Test is part of a class
                if test_class not in file_entry["classes"]:
                    file_entry["classes"][test_class] = {"tests": [], "markers": set()}

                file_entry["classes"][test_class]["tests"].append(
                    {
                        "name": test_name,
                        "id": test.get("id", ""),
                        "markers": test.get("markers", []),
                    }
                )

                # Add markers to class set
                for marker in test.get("markers", []):
                    file_entry["classes"][test_class]["markers"].add(marker)

            else:
                # Test is a standalone function
                file_entry["functions"].append(
                    {
                        "name": test_name,
                        "id": test.get("id", ""),
                        "markers": test.get("markers", []),
                    }
                )

        # Convert marker sets to lists for JSON serialization
        for _file_path, file_data in hierarchy.items():
            for _class_name, class_data in file_data["classes"].items():
                class_data["markers"] = list(class_data["markers"])

        return hierarchy

    def _generate_summary(self, tests: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Generate summary statistics from test list.

        Args:
            tests: List of test dictionaries

        Returns:
            Summary dictionary with counts and statistics
        """
        total = len(tests)
        by_marker: dict[str, int] = {}
        files = set()

        for test in tests:
            # Count markers
            for marker in test.get("markers", []):
                by_marker[marker] = by_marker.get(marker, 0) + 1

            # Collect unique files
            if "path" in test:
                files.add(test["path"])

        return {
            "total": total,
            "by_marker": by_marker,
            "files": files,
            "file_count": len(files),
        }
