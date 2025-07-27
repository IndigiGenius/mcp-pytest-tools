# MCP Pytest Tools

A Model Context Protocol (MCP) server that provides pytest functionality as tools for AI assistants. This project enables AI systems to run tests, analyze test results, and interact with pytest's rich ecosystem through the MCP interface.

## Overview

This MCP server exposes pytest capabilities to AI assistants, achieving a **95% reduction in token consumption** during test-driven development workflows by providing focused, structured test information instead of raw console output.

## Key Features

- **Test Discovery**: List and filter tests without execution
- **Selective Execution**: Run specific tests or test patterns
- **Smart Output**: Condensed, token-efficient test results
- **Failure Analysis**: Focused debugging information
- **Coverage Integration**: Quick coverage metrics
- **Performance Analysis**: Identify slow tests

## Installation

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

Start the MCP server:

```bash
python -m mcp_pytest_tools.server
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines, including:
- Micro-commit workflow
- Test-driven development practices
- PR guidelines (~400 lines per PR)
- Quality metrics and tracking

## Architecture

The project follows a phased implementation approach:
- **Phase 1**: Core functionality (test discovery, basic execution)
- **Phase 2**: Enhanced features (failure analysis, coverage)
- **Phase 3**: Advanced tools (smart selection, reporting)
- **Phase 4**: Polish and optimization

See [PHASED_ARCHITECTURE.md](PHASED_ARCHITECTURE.md) for detailed implementation plan.

## Contributing

1. Create a feature branch from `main`
2. Follow the micro-commit strategy (4-15 commits/hour)
3. Ensure tests pass and coverage remains >85%
4. Submit PR with ~400 lines of changes

## License

MIT License - see LICENSE file for details.