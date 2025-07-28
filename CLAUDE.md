# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**mcp-pytest-tools** is a Model Context Protocol (MCP) implementation that provides pytest functionality as tools for AI assistants. This project enables AI systems to run tests, analyze test results, and interact with pytest's rich ecosystem through the MCP interface.

Primary objectives:
- Expose pytest functionality through MCP tools
- Enable AI assistants to run and analyze tests
- Provide structured test result output for AI consumption

Target audience: Developers using AI assistants for test-driven development and test automation.

## Development Commands

### Environment Setup
```bash
# Install dependencies using UV (preferred)
uv sync

# Alternative: pip setup
# pip install -e .

# Set up pre-commit hooks for micro-commit workflow
uv add --dev pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Running the Application
```bash
# Start the MCP server
python -m mcp_pytest_tools.server

# With specific configuration
python -m mcp_pytest_tools.server --config config.json
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mcp_pytest_tools --cov-report=html

# Run specific test file
uv run pytest tests/test_server.py

# Run tests with verbose output
uv run pytest -v
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy mcp_pytest_tools/
```

### Pre-Commit Workflow
**IMPORTANT**: Always run these commands in order before committing:

```bash
# 1. Format code (fixes formatting issues automatically)
uv run ruff format .

# 2. Lint code (checks for code quality issues)
uv run ruff check .

# 3. Type check (ensures type safety)
uv run mypy mcp_pytest_tools/

# 4. Run tests (ensures functionality works)
uv run pytest

# 5. Check coverage (optional but recommended)
uv run pytest --cov=mcp_pytest_tools --cov-report=term-missing
```

**CI Pipeline Order**: The GitHub Actions CI runs these same steps in the same order. Running them locally first prevents CI failures.

## Architecture Overview

### Core Components
- **MCP Server**: Main server implementation handling MCP protocol communication
- **Pytest Runner**: Wrapper around pytest for executing tests and capturing results
- **Result Parser**: Converts pytest output into structured MCP responses
- **Tool Registry**: Manages available pytest-related tools exposed via MCP

### Expected Project Structure
```
mcp-pytest-tools/
├── mcp_pytest_tools/     # Main source code
│   ├── server.py         # MCP server implementation
│   ├── tools/            # Individual tool implementations
│   ├── runner.py         # Pytest execution wrapper
│   └── parser.py         # Result parsing utilities
├── tests/                # Test files
├── docs/                 # Documentation
├── examples/             # Example usage and configurations
└── pyproject.toml        # Project configuration
```

### Tech Stack
- Language: Python 3.9+
- Key Libraries: pytest, mcp, asyncio, pydantic
- Tools: UV, pytest, ruff, mypy

## Development Methodology

### Test-Driven Development (TDD)
This project follows TDD principles:
1. **Red**: Write a failing test that defines expected behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests passing

#### AI-Assisted Test Generation
- Use Claude Code to generate comprehensive test suites: "Generate pytest tests for [function] including edge cases for [specific scenarios]"
- Target 85%+ code coverage with meaningful tests
- Use property-based testing (Hypothesis) for edge case discovery
- Run tests in parallel with pytest-xdist for faster feedback

### Git Workflow
- **Always create a new branch** for features/fixes
- Branch naming: `feature/description`, `fix/description`, `docs/description`
- Never commit directly to main

#### Micro-Commit Strategy
- **Commit frequency**: Target 4-15 commits per hour during active development
- **Commit size**: Keep changes to 20-50 lines per commit
- **Atomic changes**: Each commit should represent ONE logical change:
  - A single function implementation
  - A variable rename across files
  - Adding one test case
  - Fixing one specific bug
- **Example for MCP tools**: 
  1. Commit 1: Add tool interface definition
  2. Commit 2: Implement input validation
  3. Commit 3: Add core functionality
  4. Commit 4: Add error handling
  5. Commit 5: Add tests for the tool

### Pull Request Guidelines
- **Keep PRs focused and manageable**: Target ~400 lines of code changes (see PHASED_ARCHITECTURE.md)
- Large features should be broken into multiple smaller PRs
- Each PR should represent one logical change
- Include tests for new functionality (counts toward line limit)
- Update documentation as needed

#### Risk-Based Review Strategy
- **Auto-merge candidates** (after CI passes):
  - Pure formatting changes
  - Test additions with no logic changes
  - Documentation updates
- **Light review** (1 reviewer):
  - Minor refactors
  - Dependency updates
  - Non-critical bug fixes
- **Full review** (2+ reviewers):
  - New MCP tool implementations
  - Changes to core server logic
  - Security-related modifications

### Code Style
- Python 3.x with type hints
- Google-style docstrings
- Meaningful variable and function names
- Keep functions small and focused
- DRY (Don't Repeat Yourself) principle

### Claude Code Workflow Optimization

#### Think-Plan-Code-Commit Pattern
When working with Claude Code, structure your requests as:
1. **Research phase**: "Analyze the existing [component] in [path]"
2. **Planning phase**: "Create a detailed plan for [specific goal]"
3. **Implementation**: "Implement step [N] of the plan - [specific task]"
4. **Commit**: "Create a micro-commit with conventional commit message"

##### MCP Pytest Tools Examples:
```
1. Research: "Analyze how pytest collects tests in pytest source code"
2. Plan: "Create a plan for implementing the list_tests MCP tool"
3. Implement: "Implement the test discovery parser in parsers/collector.py"
4. Test: "Generate comprehensive tests for the list_tests tool including edge cases"
5. Commit: "Create a micro-commit for the test discovery implementation"
```

#### Multi-Agent Development
For complex features, use multiple Claude Code instances in parallel:
- Terminal 1: Core feature implementation
- Terminal 2: Test development
- Terminal 3: Documentation updates
- Terminal 4: Integration and refactoring

Each agent maintains focused context for better results.

## Project Status

### Current Focus 🎯
Initial project setup and core MCP server implementation

### Completed ✅
- [x] Repository initialization
- [x] CLAUDE.md creation

### In Progress 🚧
- [ ] Basic MCP server structure
- [ ] Pytest runner implementation
- [ ] Initial tool definitions

### Roadmap 🗺️
1. **Phase 1**: Foundation - Core MCP server with basic tools (5 PRs, ~2000 lines)
2. **Phase 2**: Enhanced Functionality - Failure analysis and coverage (4 PRs, ~1600 lines)
3. **Phase 3**: Advanced Features - Smart selection and reporting (4 PRs, ~1600 lines)
4. **Phase 4**: Polish - Optimization and documentation (3 PRs, ~1200 lines)

See PHASED_ARCHITECTURE.md for detailed implementation plan with ~400 lines per PR.

## Recommended Development Tools

### Code Quality & Speed
- **Ruff**: Fast Python linter and formatter (replaces Black, isort, flake8)
  ```bash
  uv run ruff format .  # Format code
  uv run ruff check .   # Lint code
  ```

### Testing Acceleration
- **pytest-xdist**: Parallel test execution
  ```bash
  uv run pytest -n auto  # Run tests in parallel
  ```
- **Hypothesis**: Property-based testing for edge cases
- **mutmut**: Mutation testing to validate test effectiveness

### Commit Automation
- **Conventional Commits**: Use clear, structured commit messages
- **Claude Code Integration**: Already handles commit message generation with appropriate context

### Multi-Repository Management
- **mani CLI**: Lightweight tool for managing multiple repos
- **GitKraken Workspaces**: Visual management for complex projects

## CI/CD and Quality Gates

### GitHub Actions Setup
Create `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install uv
      - run: uv sync
      - run: uv run pytest --cov
      - run: uv run ruff check .
      - run: uv run mypy mcp_pytest_tools/
```

### Quality Gates
- **Auto-merge eligible**: Coverage ≥85%, all tests pass, no linting errors
- **Manual review required**: Coverage drops >5%, new public APIs

## Development Metrics

### Velocity Tracking
```bash
# Weekly commit count
git log --since="1 week ago" --oneline | wc -l

# Average PR cycle time (using gh CLI)
gh pr list --state merged --limit 10 --json createdAt,mergedAt
```

### Key Metrics to Monitor
- **Commit frequency**: Target 50+ micro-commits/week during active development
- **PR cycle time**: Target <24 hours from creation to merge
- **Test coverage**: Maintain >85%
- **Build success rate**: Target >95%

## Common Tasks

### Adding a New MCP Tool
1. Create a new branch from main
2. Write tests for the tool functionality
3. Implement the tool in `mcp_pytest_tools/tools/`
4. Register the tool in the server
5. Update documentation
6. Create PR for review

### Debugging MCP Communication
1. Enable debug logging in the server
2. Check MCP protocol messages in logs
3. Use MCP inspector tools
4. Verify tool registration and schemas

### Testing MCP Tools
```bash
# Test individual tools
uv run pytest tests/tools/test_specific_tool.py

# Test with MCP client
python -m mcp_pytest_tools.test_client
```

## Important Notes

### Do's ✅
- Write tests before implementing features
- Keep MCP tool interfaces simple and focused
- Provide clear error messages in tool responses
- Document tool parameters and return values
- Handle pytest exceptions gracefully

### Don'ts ❌
- Don't expose system-level commands through MCP
- Don't allow arbitrary code execution
- Don't ignore pytest security warnings
- Don't return raw pytest internals in responses
- Don't create tools with side effects beyond test execution

## Project-Specific Guidelines

### MCP Tool Design
- Each tool should have a single, clear purpose
- Tool names should be descriptive and follow naming conventions
- Always validate input parameters
- Return structured data suitable for AI consumption

### Pytest Integration
- Respect pytest configuration files (pytest.ini, setup.cfg)
- Support common pytest plugins
- Preserve pytest's exit codes and signals
- Handle test collection errors gracefully

---

Last Updated: 2025-07-27
Version: 1.1
Changes: Added micro-commit strategy, Claude Code workflow optimization, AI-assisted testing, and recommended development tools