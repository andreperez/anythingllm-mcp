# Contributing to AnythingLLM MCP Server

Thank you for your interest in contributing to the AnythingLLM MCP Server! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows the principles of respect, inclusivity, and collaborative problem-solving. We expect all contributors to:

- Be respectful and constructive in discussions
- Focus on what is best for the project and the community
- Show empathy towards other contributors
- Accept constructive criticism gracefully

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/anythingllm-mcp.git
   cd anythingllm-mcp
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/andreperez/anythingllm-mcp.git
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- AnythingLLM instance running (for integration testing)

### Installation

1. Install dependencies:
   ```bash
   uv sync --extra dev
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your AnythingLLM API key and base URL
   ```

3. Run tests to verify setup:
   ```bash
   uv run pytest
   ```

## How to Contribute

### Types of Contributions

We welcome:

- **Bug fixes**: Fix issues reported in the issue tracker
- **New features**: Add new tools or capabilities
- **Documentation**: Improve README, docstrings, or guides
- **Tests**: Expand test coverage
- **Performance improvements**: Optimize existing code
- **Code quality**: Refactoring, type hints, error handling

### Before You Start

1. **Check existing issues**: See if someone is already working on it
2. **Open an issue**: For significant changes, discuss your approach first
3. **Create a feature branch**: Work on a descriptive branch name
   ```bash
   git checkout -b feature/add-workspace-permissions
   git checkout -b fix/timeout-error-handling
   ```

## Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all public functions (Google style)
- Maximum line length: **100 characters**

### Code Organization

- Keep functions focused and single-purpose
- Use async/await for I/O operations
- Group related tools together
- Maintain the existing file structure

### Example Function

```python
@mcp.tool(
    name="anythingllm_example_tool",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    },
)
async def example_tool(param: str, optional_param: int = 10) -> str:
    """
    Brief description of what the tool does.

    Args:
        param: Description of the parameter
        optional_param: Description with default value (default: 10)

    Returns:
        JSON string with the tool result

    Raises:
        ValueError: When param is invalid
    """
    try:
        # Implementation
        result = await _api(f"/endpoint/{param}")
        return _json_response(result)
    except Exception as e:
        return _handle_error(e)
```

### Annotations

Use tool annotations to describe behavior:

- `readOnlyHint`: Tool only reads data, no modifications
- `destructiveHint`: Tool deletes or irreversibly modifies data
- `idempotentHint`: Safe to call multiple times with same args
- `openWorldHint`: Tool makes external HTTP requests

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/test_anythingllm_mcp.py

# Run specific test
uv run pytest tests/test_anythingllm_mcp.py::test_require_api_key
```

### Writing Tests

- Use `pytest` conventions
- Mock HTTP calls with `respx`
- Test both success and error paths
- Include edge cases

Example test:

```python
import pytest
import respx
from httpx import Response

@respx.mock
@pytest.mark.asyncio
async def test_list_workspaces_success(mcp_server):
    """Test successful workspace listing."""
    respx.get(f"{API_BASE_URL}/api/v1/workspaces").mock(
        return_value=Response(200, json={
            "workspaces": [
                {"name": "Test", "slug": "test"}
            ]
        })
    )
    
    result = await list_workspaces()
    assert "Test" in result
    assert "test" in result
```

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**: Ensure all tests pass
   ```bash
   uv run pytest
   ```

3. **Run linting** (if configured):
   ```bash
   uv run ruff check .
   uv run mypy .
   ```

4. **Update documentation**: If you changed behavior or added features

### Commit Messages

Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(chat): add streaming support for chat responses
fix(auth): handle missing API key gracefully
docs(readme): update installation instructions
test(workspaces): add tests for workspace deletion
```

### Pull Request Template

When opening a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added tests for new functionality
- [ ] Tested manually with AnythingLLM instance

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)
```

## Reporting Issues

### Bug Reports

Include:

1. **Environment information**:
   - Python version (`python --version`)
   - uv version (`uv --version`)
   - AnythingLLM version
   - OS

2. **Steps to reproduce**:
   ```
   1. Run server with: uv run anythingllm-mcp
   2. Call tool: anythingllm_create_workspace
   3. Observe error: ...
   ```

3. **Expected vs. actual behavior**

4. **Error messages and logs** (sanitize API keys!)

### Feature Requests

Include:

1. **Use case**: Why is this feature needed?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches you thought about
4. **AnythingLLM API support**: Does the API support this?

## Development Tips

### Local Testing with MCP Clients

Test your changes in a real MCP client:

```bash
# VS Code: Update mcp.json to point to your local clone
{
  "servers": {
    "anythingllm-dev": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/clone/anythingllm-mcp",
        "anythingllm-mcp"
      ],
      "env": {
        "ANYTHINGLLM_API_KEY": "your-key",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
      }
    }
  }
}
```

### Debugging

Set environment variable for verbose logging:

```bash
export FASTMCP_DEBUG=true
export FASTMCP_LOG_LEVEL=DEBUG
```

### Hot Reload During Development

The MCP client will restart the server on file changes. No need to manually restart.

## Questions?

If you have questions:

1. Check existing [issues](https://github.com/andreperez/anythingllm-mcp/issues)
2. Review [README.md](README.md) and other documentation
3. Open a [discussion](https://github.com/andreperez/anythingllm-mcp/discussions) or issue

Thank you for contributing! 🎉
