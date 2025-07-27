# MCP Pytest Tools Implementation Plan

## Quick Summary

The most token-efficient pytest tools for an AI assistant are:

1. **`list_tests`** - Show available tests without running them (~200 tokens vs ~10,000)
2. **`run_test`** - Execute specific tests with summary output (~300 tokens vs ~2,000)
3. **`show_failures`** - Display only failed test info (~100 tokens per failure)
4. **`rerun_failed`** - Re-execute only previously failed tests
5. **`get_coverage`** - Return coverage percentage only (~50 tokens vs ~5,000)

## Proposed MCP Tools

### 1. Essential Tools (Phase 1)

```python
# Tool 1: List Tests
async def list_tests(
    path: Optional[str] = None,
    pattern: Optional[str] = None,
    marker: Optional[str] = None
) -> TestListResult:
    """
    Discover tests without execution.
    Returns: List of test modules, classes, and functions
    Token savings: ~98% compared to running all tests
    """

# Tool 2: Run Specific Test
async def run_test(
    test_path: str,  # e.g., "tests/test_module.py::TestClass::test_method"
    verbose: bool = False,
    stop_on_failure: bool = True
) -> TestResult:
    """
    Run a single test or test subset.
    Returns: Pass/fail status with optional error details
    Token savings: ~90% by avoiding full suite execution
    """

# Tool 3: Run Tests by Pattern
async def run_tests_matching(
    pattern: str,  # e.g., "test_*_integration"
    max_failures: Optional[int] = 1,
    output: Literal["summary", "short", "full"] = "summary"
) -> TestSuiteResult:
    """
    Run tests matching a pattern.
    Returns: Summary with failure details only
    Token savings: ~85% with summary mode
    """

# Tool 4: Show Only Failures
async def get_test_failures(
    from_last_run: bool = True,
    include_traceback: bool = True,
    traceback_style: Literal["short", "long", "line"] = "short"
) -> FailureReport:
    """
    Get details of failed tests only.
    Returns: Focused failure information
    Token savings: ~95% by skipping passed tests
    """
```

### 2. Efficiency Tools (Phase 2)

```python
# Tool 5: Quick Test Status
async def get_test_summary(
    path: Optional[str] = None
) -> TestSummary:
    """
    Get test counts without details.
    Returns: {"passed": N, "failed": N, "skipped": N, "duration": N}
    Token savings: ~99% - just the numbers
    """

# Tool 6: Coverage Summary
async def get_coverage_summary(
    path: Optional[str] = None
) -> CoverageSummary:
    """
    Get coverage percentage only.
    Returns: {"total": 85.5, "by_module": {...}}
    Token savings: ~98% vs full coverage report
    """

# Tool 7: Find Slow Tests
async def find_slow_tests(
    top_n: int = 10,
    threshold_seconds: float = 1.0
) -> SlowTestReport:
    """
    Identify performance bottlenecks.
    Returns: List of slow tests with durations
    Token savings: Focused data instead of full run
    """
```

### 3. Smart Tools (Phase 3)

```python
# Tool 8: Test Impact Analysis
async def find_affected_tests(
    changed_files: List[str]
) -> AffectedTests:
    """
    Find tests affected by code changes.
    Returns: Tests that should be run
    Token savings: ~80% by running only relevant tests
    """

# Tool 9: Flaky Test Detection
async def find_flaky_tests(
    iterations: int = 3
) -> FlakyTestReport:
    """
    Identify unreliable tests.
    Returns: Tests with inconsistent results
    Token savings: Targeted reliability analysis
    """
```

## Token Consumption Examples

### Scenario 1: Debugging a Failed Test
**Traditional approach** (20,000+ tokens):
```
1. Run all tests → 10,000 tokens
2. See failure in verbose output → 5,000 tokens  
3. Re-run with more debugging → 5,000 tokens
```

**Optimized approach** (500 tokens):
```
1. list_tests(pattern="failing") → 50 tokens
2. run_test("tests/test_module.py::test_failing") → 200 tokens
3. get_test_failures(traceback_style="short") → 250 tokens
```

### Scenario 2: Checking Test Coverage
**Traditional approach** (5,000+ tokens):
```
Full coverage report with line-by-line details
```

**Optimized approach** (50 tokens):
```
get_coverage_summary() → {"total": 85.5, "untested_modules": 3}
```

## Implementation Architecture

```
mcp_pytest_tools/
├── server.py           # MCP server setup
├── tools/
│   ├── discovery.py    # list_tests, find_affected_tests
│   ├── execution.py    # run_test, run_tests_matching
│   ├── reporting.py    # get_test_failures, get_test_summary
│   └── analysis.py     # get_coverage_summary, find_slow_tests
├── parsers/
│   ├── output.py       # Parse pytest output efficiently
│   └── traceback.py    # Condense traceback information
└── cache.py            # Cache test results to avoid re-runs
```

## Key Design Decisions

1. **Default to Summary Mode**: All tools return minimal information by default
2. **Structured Output**: Use dataclasses/TypedDict for predictable, efficient responses
3. **Incremental Detail**: Allow drilling down into specifics only when requested
4. **Result Caching**: Cache test outcomes to avoid redundant executions
5. **Streaming for Large Output**: Stream results for long-running operations

## Success Metrics

- **Token Reduction**: >90% reduction in typical debugging sessions
- **Time to First Result**: <2 seconds for most operations
- **User Satisfaction**: Fewer round trips to get needed information
- **Coverage**: Support 90% of common pytest workflows

This implementation would provide AI assistants with powerful pytest capabilities while dramatically reducing token consumption, making test-driven development more efficient and cost-effective.