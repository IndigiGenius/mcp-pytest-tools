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

### Git Workflow
- **Always create a new branch** for features/fixes
- Branch naming: `feature/description`, `fix/description`, `docs/description`
- Never commit directly to main

### Pull Request Guidelines
- **Keep PRs focused and manageable**: Target ~400 lines of code changes (see PHASED_ARCHITECTURE.md)
- Large features should be broken into multiple smaller PRs
- Each PR should represent one logical change
- Include tests for new functionality (counts toward line limit)
- Update documentation as needed

### Code Style
- Python 3.x with type hints
- Google-style docstrings
- Meaningful variable and function names
- Keep functions small and focused
- DRY (Don't Repeat Yourself) principle

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

Last Updated: 2025-07-26
Version: 1.0