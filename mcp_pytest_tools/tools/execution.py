"""Test execution tool for running pytest tests."""

import subprocess
import time
from datetime import datetime
from typing import Any

from mcp_pytest_tools.models import TestExecutionResult
from mcp_pytest_tools.parsers.output import PytestOutputParser


class TestExecutionTool:
    """Tool for executing individual pytest tests."""

    def __init__(self) -> None:
        """Initialize the test execution tool."""
        self.name = "run_test"
        self.description = "Execute a single test or test file and capture results"
        self.parameters = {
            "test_path": {
                "type": "string",
                "description": "Path to the test to execute (file or file::test)",
                "required": True,
            },
            "timeout": {
                "type": "number",
                "description": "Timeout in seconds for test execution",
                "required": False,
                "default": 30,
            },
            "capture_output": {
                "type": "boolean",
                "description": "Whether to capture stdout and stderr",
                "required": False,
                "default": True,
            },
        }
        self.output_parser = PytestOutputParser()

    async def execute_test(
        self,
        test_path: str,
        timeout: int = 30,
        capture_output: bool = True,
        pytest_args: list[str] | None = None,
    ) -> TestExecutionResult:
        """
        Execute a pytest test and return structured results.

        Args:
            test_path: Path to the test to execute
            timeout: Timeout in seconds
            capture_output: Whether to capture output
            pytest_args: Additional pytest arguments

        Returns:
            TestExecutionResult with execution details
        """
        started_at = datetime.now()

        # Build command
        cmd = self._build_command(test_path, pytest_args)

        # Execute test
        try:
            start_time = time.time()

            if capture_output:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=timeout
                )
                stdout = result.stdout or ""
                stderr = result.stderr or ""
            else:
                result = subprocess.run(
                    cmd, capture_output=False, text=True, timeout=timeout
                )
                stdout = ""
                stderr = ""

            duration = time.time() - start_time

        except subprocess.TimeoutExpired:
            completed_at = datetime.now()
            return TestExecutionResult(
                test_path=test_path,
                status="timeout",
                exit_code=-1,
                stdout="",
                stderr="",
                duration=timeout,
                started_at=started_at,
                completed_at=completed_at,
                error_message=f"Test execution timed out after {timeout} seconds",
            )

        completed_at = datetime.now()

        # Determine status from exit code
        error_message = None
        if result.returncode == 0:
            status = "passed"
        elif result.returncode == 1:
            status = "failed"
        elif result.returncode == 4:
            status = "error"
            error_message = "No tests collected or test not found"
        else:
            status = "error"
            error_message = f"Unexpected exit code: {result.returncode}"

        # Parse output for additional details
        # TODO: Use parsed output to enhance result details
        _ = self._parse_output(stdout, stderr)

        return TestExecutionResult(
            test_path=test_path,
            status=status,
            exit_code=result.returncode,
            stdout=stdout,
            stderr=stderr,
            duration=duration,
            started_at=started_at,
            completed_at=completed_at,
            error_message=error_message if status == "error" else None,
        )

    def _build_command(
        self, test_path: str, pytest_args: list[str] | None = None
    ) -> list[str]:
        """Build pytest command with arguments."""
        cmd = ["python", "-m", "pytest", "-v", test_path]

        if pytest_args:
            cmd.extend(pytest_args)

        return cmd

    def _parse_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse pytest output for test details."""
        return self.output_parser.parse_test_output(stdout, stderr)
