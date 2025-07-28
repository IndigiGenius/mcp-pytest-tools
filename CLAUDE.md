# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**mcp-pytest-tools** is an MCP implementation that provides pytest functionality as tools for AI assistants.

Primary objectives:
- Expose pytest functionality through MCP tools
- Enable AI assistants to run tests and analyze results
- Provide structured test result output for AI consumption

## Development Commands

### Environment & Server
```bash
# Setup
uv sync
pre-commit install

# Run MCP server
python -m mcp_pytest_tools.server
```

### Testing & Quality
```bash
# Tests
uv run pytest
uv run pytest --cov=mcp_pytest_tools --cov-report=html

# Quality (use --quiet to save tokens)
uv run ruff format . --quiet
uv run ruff check . --quiet
uv run mypy mcp_pytest_tools/
```

### Pre-Commit Workflow
**REQUIRED order before committing:**
1. `uv run ruff format . --quiet`
2. `uv run ruff check . --quiet`
3. `uv run mypy mcp_pytest_tools/`
4. `uv run pytest`

## Architecture

### Core Components
- **MCP Server**: Protocol communication handler
- **Pytest Runner**: Test execution wrapper
- **Result Parser**: Converts pytest output to structured MCP responses
- **Tool Registry**: Manages available tools

### Project Structure
```
mcp_pytest_tools/
├── server.py         # MCP server
├── tools/            # Tool implementations
├── parsers/          # Output parsing
├── models.py         # Pydantic models
└── exceptions.py     # Error handling
```

### Tech Stack
- Python 3.10+, pytest, mcp, asyncio, pydantic
- Tools: UV, ruff, mypy

## Development Methodology

### TDD Process
1. **Red**: Write failing test
2. **Green**: Minimal code to pass
3. **Refactor**: Improve while keeping tests green

Target 85%+ coverage with meaningful tests.

### Git Workflow
- Always create feature branches: `feature/description`
- Never commit to main
- **Micro-commits**: 4-15 commits/hour, 20-50 lines each
- **PR size**: ~400 lines (see PHASED_ARCHITECTURE.md)

### Code Style
- Python 3.x with type hints
- Google-style docstrings
- Keep functions small and focused
- Use meaningful names

## Project Status

See PHASED_ARCHITECTURE.md for detailed implementation plan:
1. **Phase 1**: Foundation (5 PRs, ~2000 lines)
2. **Phase 2**: Enhanced Functionality (4 PRs, ~1600 lines) 
3. **Phase 3**: Advanced Features (4 PRs, ~1600 lines)
4. **Phase 4**: Polish (3 PRs, ~1200 lines)
5. **Phase 5**: Quality Assurance (4 PRs, ~1550 lines)

## Quality Gates

### CI Requirements
- Coverage ≥85%
- All tests pass
- No linting/type errors
- Auto-merge for: formatting, tests, docs
- Manual review for: new tools, core changes, security

### Key Metrics
- 50+ micro-commits/week during development
- <24 hour PR cycle time
- >95% build success rate

## Common Tasks

### Adding MCP Tool
1. Create branch
2. Write tests first
3. Implement in `tools/`
4. Register in server
5. Create PR

### Testing Tools
```bash
uv run pytest tests/tools/test_specific_tool.py
python -m mcp_pytest_tools.test_client
```

## Important Guidelines

### Do's ✅
- Tests before features
- Simple MCP tool interfaces
- Clear error messages
- Validate input parameters
- Handle pytest exceptions gracefully

### Don'ts ❌
- System-level commands through MCP
- Arbitrary code execution
- Raw pytest internals in responses
- Tools with side effects beyond test execution

### MCP Tool Design
- Single, clear purpose per tool
- Descriptive naming
- Structured data output for AI consumption
- Respect pytest configuration files

---

Last Updated: 2025-07-28
Version: 1.2 - Optimized for token efficiency