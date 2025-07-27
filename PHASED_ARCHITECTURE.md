# Phased Architecture Implementation Plan

## Overview
This document outlines a phased approach to implementing mcp-pytest-tools with each phase containing approximately 400 lines of code. This ensures manageable pull requests, easier code reviews, and incremental value delivery.

## Architecture Principles
1. **Small, Focused Changes**: Each PR implements one complete feature
2. **Always Deployable**: Every phase results in working software
3. **Test-First**: Each phase includes tests (counting toward the 400-line limit)
4. **Incremental Value**: Users can benefit from each phase immediately

## Phase 1: Foundation (5 PRs, ~2000 lines total)

### PR 1.1: Project Setup and Core Structure (~350 lines)
**Goal**: Establish project foundation with basic MCP server

**Files**:
```
pyproject.toml                    # 50 lines
mcp_pytest_tools/__init__.py      # 10 lines
mcp_pytest_tools/server.py        # 150 lines (basic MCP server)
mcp_pytest_tools/models.py        # 80 lines (pydantic models)
tests/test_server.py              # 60 lines
```

**Key Components**:
- Basic MCP server setup with health check
- Core pydantic models for request/response
- Test infrastructure setup
- UV/pytest configuration

### PR 1.2: Test Discovery Tool (~400 lines)
**Goal**: Implement `list_tests` functionality

**Files**:
```
mcp_pytest_tools/tools/__init__.py           # 10 lines
mcp_pytest_tools/tools/discovery.py          # 180 lines
mcp_pytest_tools/parsers/__init__.py         # 10 lines
mcp_pytest_tools/parsers/collector.py        # 120 lines
tests/test_discovery.py                       # 80 lines
```

**Features**:
- Pytest collection without execution
- Parse collected tests into structured format
- Support path, pattern, and marker filtering
- Return hierarchical test structure

### PR 1.3: Basic Test Execution (~400 lines)
**Goal**: Implement `run_test` for single test execution

**Files**:
```
mcp_pytest_tools/tools/execution.py          # 200 lines
mcp_pytest_tools/parsers/output.py           # 100 lines
mcp_pytest_tools/models.py                   # +50 lines (new models)
tests/test_execution.py                       # 50 lines
```

**Features**:
- Run individual test by path
- Capture pass/fail status
- Basic output parsing
- Timeout handling

### PR 1.4: Error Handling and Logging (~380 lines)
**Goal**: Robust error handling across all tools

**Files**:
```
mcp_pytest_tools/exceptions.py               # 80 lines
mcp_pytest_tools/logger.py                   # 100 lines
mcp_pytest_tools/server.py                   # +50 lines (error handlers)
mcp_pytest_tools/tools/base.py               # 100 lines (base tool class)
tests/test_error_handling.py                 # 50 lines
```

**Features**:
- Custom exception hierarchy
- Structured logging with context
- Graceful error recovery
- User-friendly error messages

### PR 1.5: Summary Reporting Tool (~370 lines)
**Goal**: Implement `get_test_summary` for quick status

**Files**:
```
mcp_pytest_tools/tools/reporting.py          # 150 lines
mcp_pytest_tools/parsers/summary.py          # 120 lines
mcp_pytest_tools/cache.py                    # 80 lines (basic caching)
tests/test_reporting.py                      # 20 lines
```

**Features**:
- Quick test count summary
- Execution time tracking
- Basic result caching
- Structured summary format

## Phase 2: Enhanced Functionality (4 PRs, ~1600 lines)

### PR 2.1: Failure Analysis Tool (~400 lines)
**Goal**: Implement `get_test_failures` with smart traceback

**Files**:
```
mcp_pytest_tools/tools/failures.py           # 180 lines
mcp_pytest_tools/parsers/traceback.py        # 150 lines
mcp_pytest_tools/models.py                   # +30 lines
tests/test_failures.py                       # 40 lines
```

**Features**:
- Extract failure information
- Configurable traceback styles (short/long/line)
- Failure categorization
- Smart error message extraction

### PR 2.2: Pattern-Based Test Execution (~390 lines)
**Goal**: Implement `run_tests_matching` for batch execution

**Files**:
```
mcp_pytest_tools/tools/execution.py          # +150 lines
mcp_pytest_tools/tools/filters.py            # 120 lines
mcp_pytest_tools/models.py                   # +40 lines
tests/test_pattern_execution.py              # 80 lines
```

**Features**:
- Keyword-based test selection
- Marker-based filtering
- Max failure limits
- Batch execution optimization

### PR 2.3: Coverage Integration (~400 lines)
**Goal**: Implement `get_coverage_summary` tool

**Files**:
```
mcp_pytest_tools/tools/coverage.py           # 200 lines
mcp_pytest_tools/parsers/coverage.py         # 120 lines
mcp_pytest_tools/config.py                   # 40 lines
tests/test_coverage.py                       # 40 lines
```

**Features**:
- Coverage percentage extraction
- Module-level breakdown
- Coverage trend tracking
- Integration with pytest-cov

### PR 2.4: Performance Analysis (~410 lines)
**Goal**: Implement `find_slow_tests` tool

**Files**:
```
mcp_pytest_tools/tools/performance.py        # 180 lines
mcp_pytest_tools/parsers/duration.py         # 100 lines
mcp_pytest_tools/cache.py                    # +50 lines (enhanced)
tests/test_performance.py                    # 80 lines
```

**Features**:
- Duration tracking
- Slow test identification
- Performance trend analysis
- Configurable thresholds

## Phase 3: Advanced Features (4 PRs, ~1600 lines)

### PR 3.1: Smart Test Selection (~400 lines)
**Goal**: Implement `find_affected_tests` for change-based testing

**Files**:
```
mcp_pytest_tools/tools/impact.py             # 200 lines
mcp_pytest_tools/analyzers/__init__.py       # 10 lines
mcp_pytest_tools/analyzers/dependency.py     # 140 lines
tests/test_impact.py                         # 50 lines
```

**Features**:
- Git integration for change detection
- Import graph analysis
- Test-to-code mapping
- Smart test selection

### PR 3.2: Last Failed and Rerun (~380 lines)
**Goal**: Implement `rerun_failed` functionality

**Files**:
```
mcp_pytest_tools/tools/rerun.py              # 160 lines
mcp_pytest_tools/state.py                    # 120 lines
mcp_pytest_tools/models.py                   # +40 lines
tests/test_rerun.py                          # 60 lines
```

**Features**:
- Failed test tracking
- State persistence
- Intelligent rerun strategies
- Failure history

### PR 3.3: Structured Output Formats (~390 lines)
**Goal**: JSON and JUnit report generation

**Files**:
```
mcp_pytest_tools/tools/export.py             # 180 lines
mcp_pytest_tools/formatters/__init__.py      # 10 lines
mcp_pytest_tools/formatters/json.py          # 80 lines
mcp_pytest_tools/formatters/junit.py         # 80 lines
tests/test_export.py                         # 40 lines
```

**Features**:
- Multiple output formats
- CI/CD integration support
- Customizable reports
- Streaming for large outputs

### PR 3.4: Configuration and CLI (~430 lines)
**Goal**: Complete configuration system and CLI

**Files**:
```
mcp_pytest_tools/cli.py                      # 200 lines
mcp_pytest_tools/config.py                   # +100 lines
mcp_pytest_tools/server.py                   # +50 lines
docs/configuration.md                        # 50 lines
tests/test_cli.py                           # 30 lines
```

**Features**:
- YAML/JSON configuration
- Environment variable support
- CLI for server management
- Configuration validation

## Phase 4: Polish and Optimization (3 PRs, ~1200 lines)

### PR 4.1: Advanced Caching (~400 lines)
**Goal**: Implement intelligent result caching

**Files**:
```
mcp_pytest_tools/cache.py                    # +200 lines
mcp_pytest_tools/tools/base.py               # +50 lines
mcp_pytest_tools/config.py                   # +50 lines
tests/test_caching.py                        # 100 lines
```

**Features**:
- TTL-based cache expiration
- Cache invalidation strategies
- Memory-efficient storage
- Cache statistics

### PR 4.2: Flaky Test Detection (~380 lines)
**Goal**: Implement `find_flaky_tests` tool

**Files**:
```
mcp_pytest_tools/tools/reliability.py        # 200 lines
mcp_pytest_tools/analyzers/flaky.py          # 130 lines
tests/test_flaky.py                          # 50 lines
```

**Features**:
- Multiple run analysis
- Flakiness scoring
- Root cause hints
- Stability trends

### PR 4.3: Documentation and Examples (~420 lines)
**Goal**: Complete documentation and examples

**Files**:
```
examples/basic_usage.py                      # 80 lines
examples/advanced_usage.py                   # 100 lines
examples/ci_integration.py                   # 60 lines
docs/api_reference.md                        # 100 lines
docs/user_guide.md                           # 80 lines
```

**Features**:
- Complete API documentation
- Usage examples
- Integration guides
- Troubleshooting guide

## Success Metrics

### Code Quality Metrics
- Each PR stays within 350-430 lines
- Test coverage > 90% for each phase
- All PRs pass linting and type checking
- Documentation included with code

### Delivery Metrics
- Phase 1: 2 weeks (MVP with core functionality)
- Phase 2: 2 weeks (Enhanced features)
- Phase 3: 2 weeks (Advanced capabilities)
- Phase 4: 1 week (Polish and documentation)

### Value Delivery
- **After Phase 1**: Basic test discovery and execution (60% token savings)
- **After Phase 2**: Smart failure analysis and coverage (80% token savings)
- **After Phase 3**: Advanced features and integrations (90% token savings)
- **After Phase 4**: Production-ready with full optimization (95% token savings)

## Architecture Decisions

### Why This Breakdown?
1. **Natural Boundaries**: Each PR implements a complete feature
2. **Dependency Management**: Later phases build on earlier ones
3. **Risk Mitigation**: Core features first, advanced features later
4. **Team Velocity**: ~400 lines is 1-2 days of focused work

### Technology Choices Rationale
- **Pydantic**: Input validation and structured responses
- **AsyncIO**: Non-blocking test execution
- **UV**: Modern, fast Python package management
- **MCP Protocol**: Industry standard for AI tool integration

### Testing Strategy
- Unit tests: Included in each PR's line count
- Integration tests: Separate PR at end of each phase
- Performance tests: Phase 4 optimization
- Documentation tests: Automated with examples

This phased approach ensures steady progress with manageable changes while delivering value incrementally throughout the development process.