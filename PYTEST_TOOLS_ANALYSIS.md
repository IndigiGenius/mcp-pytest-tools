# Pytest Tools for Token Efficiency

## Overview
When working with test code through an AI assistant, token consumption can quickly escalate due to verbose test outputs, large test files, and repetitive error messages. This document outlines pytest tools that can significantly reduce token usage while maintaining or improving debugging effectiveness.

## Key Token-Saving Pytest Tools

### 1. **Test Discovery and Selection Tools**
These tools help focus on specific tests without processing entire test suites.

#### `pytest_list_tests`
- **Purpose**: List all available tests without running them
- **Token Savings**: Avoids full test execution output
- **Usage**: `pytest --collect-only -q`
- **MCP Implementation**: Return structured list of test paths and names

#### `pytest_select_tests`
- **Purpose**: Run specific tests by pattern, marker, or path
- **Token Savings**: Reduces output to only relevant tests
- **Key Options**:
  - `-k`: Select by keyword/pattern
  - `-m`: Select by marker
  - `::`: Select specific test method
- **MCP Implementation**: Accept test selectors and return focused results

### 2. **Output Control Tools**
These tools minimize verbose output while preserving essential information.

#### `pytest_summary_only`
- **Purpose**: Show only test summary without individual test output
- **Token Savings**: 80-90% reduction in output size
- **Usage**: `pytest -q` or `pytest --tb=no`
- **MCP Implementation**: Return counts and failed test names only

#### `pytest_failed_only`
- **Purpose**: Show only failed tests, skip passed ones
- **Token Savings**: Proportional to pass rate
- **Usage**: `pytest --lf` (last failed) or custom filtering
- **MCP Implementation**: Filter results to failures only

#### `pytest_short_traceback`
- **Purpose**: Condensed traceback format
- **Token Savings**: 50-70% reduction in error output
- **Usage**: `pytest --tb=short` or `--tb=line`
- **MCP Implementation**: Parse and return essential error info

### 3. **Smart Execution Tools**
These tools optimize test execution to reduce redundant processing.

#### `pytest_fail_fast`
- **Purpose**: Stop after first failure
- **Token Savings**: Avoids running remaining tests after failure
- **Usage**: `pytest -x` or `--maxfail=n`
- **MCP Implementation**: Configurable failure threshold

#### `pytest_last_failed`
- **Purpose**: Re-run only previously failed tests
- **Token Savings**: Focuses on problematic tests only
- **Usage**: `pytest --lf`
- **MCP Implementation**: Track and rerun failures

#### `pytest_changed_only`
- **Purpose**: Run tests related to changed files
- **Token Savings**: Avoids running unaffected tests
- **Usage**: Requires pytest-testmon or similar
- **MCP Implementation**: Integrate with git diff

### 4. **Analysis and Reporting Tools**
These tools provide insights without full test execution.

#### `pytest_coverage_summary`
- **Purpose**: Coverage percentage without line-by-line details
- **Token Savings**: 95% reduction vs full coverage report
- **Usage**: Custom coverage parsing
- **MCP Implementation**: Return coverage metrics only

#### `pytest_duration_report`
- **Purpose**: Identify slow tests
- **Token Savings**: Focused performance data
- **Usage**: `pytest --durations=10`
- **MCP Implementation**: Return top N slowest tests

#### `pytest_fixture_usage`
- **Purpose**: Show fixture dependencies
- **Token Savings**: Avoids reading entire test files
- **Usage**: `pytest --fixtures-per-test`
- **MCP Implementation**: Return fixture graph

### 5. **Structured Output Tools**
These tools provide machine-readable formats for efficient parsing.

#### `pytest_json_report`
- **Purpose**: JSON-formatted test results
- **Token Savings**: Structured data is more efficient to process
- **Usage**: `pytest --json-report`
- **MCP Implementation**: Return parsed JSON structure

#### `pytest_junit_xml`
- **Purpose**: JUnit XML format for CI integration
- **Token Savings**: Standardized, concise format
- **Usage**: `pytest --junit-xml=report.xml`
- **MCP Implementation**: Parse and return key metrics

## Implementation Priority

### Phase 1: Core Efficiency Tools (Highest Impact)
1. `pytest_list_tests` - Essential for test discovery
2. `pytest_select_tests` - Run specific tests only
3. `pytest_summary_only` - Minimal output mode
4. `pytest_failed_only` - Focus on failures

### Phase 2: Smart Execution
5. `pytest_fail_fast` - Stop on first failure
6. `pytest_last_failed` - Rerun failures
7. `pytest_short_traceback` - Condensed errors

### Phase 3: Advanced Analysis
8. `pytest_json_report` - Structured output
9. `pytest_coverage_summary` - Coverage metrics
10. `pytest_changed_only` - Change-based testing

## Token Consumption Comparison

### Traditional Approach
```
Running full test suite: ~10,000 tokens
Full traceback per failure: ~500 tokens
Complete coverage report: ~5,000 tokens
Total for debugging session: ~20,000+ tokens
```

### Optimized Approach
```
List tests: ~200 tokens
Run specific failed test: ~300 tokens
Short traceback: ~100 tokens
Coverage summary: ~50 tokens
Total for debugging session: ~1,000 tokens
```

**Potential Savings: 95% token reduction**

## MCP Tool Interface Design

### Example: `pytest_select_tests`
```python
{
    "name": "pytest_select_tests",
    "description": "Run specific tests with minimal output",
    "parameters": {
        "pattern": "Test name pattern (optional)",
        "marker": "Pytest marker (optional)",
        "path": "Test file or directory (optional)",
        "max_failures": "Stop after N failures (default: None)",
        "output_format": "summary|short|full (default: summary)"
    },
    "returns": {
        "passed": "Number of passed tests",
        "failed": "Number of failed tests",
        "skipped": "Number of skipped tests",
        "failures": "List of failed test details (if any)"
    }
}
```

## Best Practices for Token Efficiency

1. **Always start with test discovery** - Don't run tests blindly
2. **Use markers and patterns** - Target specific test subsets
3. **Fail fast during debugging** - Stop after first failure
4. **Request summary format by default** - Get details only when needed
5. **Cache test results** - Avoid re-running unchanged tests
6. **Parse structured output** - Use JSON/XML over plain text

## Conclusion

By implementing these pytest tools in the MCP server, we can achieve:
- **95% reduction** in token consumption for typical test sessions
- **Faster iteration** through focused test execution
- **Better debugging** with structured, relevant information
- **Improved UX** with concise, actionable outputs

The key is to provide smart defaults that minimize output while allowing users to drill down into details when needed.