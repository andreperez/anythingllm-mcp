## Description

<!-- Provide a clear and concise description of what this PR does. -->

## Related Issue

<!-- Link the issue this PR addresses. Use "Closes #123" to auto-close the issue on merge. -->

Closes #

## Type of Change

<!-- Check all that apply. -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Test improvement
- [ ] CI/CD change

## Changes Made

<!-- List the specific changes made in this PR. -->

-
-
-

## How to Test

<!-- Describe how reviewers can test your changes. -->

1.
2.
3.

## Checklist

<!-- Verify all items before requesting a review. -->

### Code Quality

- [ ] Code follows the project's [coding standards](CONTRIBUTING.md#coding-standards)
- [ ] Type hints are included for all function parameters and return values
- [ ] Docstrings follow Google style format
- [ ] No hardcoded API keys, secrets, or credentials

### Testing

- [ ] New tests added for changed functionality
- [ ] All existing tests pass: `uv run pytest`
- [ ] Tests cover edge cases and error scenarios

### Documentation

- [ ] README updated (if applicable)
- [ ] CHANGELOG updated with the change
- [ ] Docstrings updated for modified functions

### MCP Tools (if adding/modifying tools)

- [ ] Tool has proper `@mcp.tool()` decorator with annotations
- [ ] `readOnlyHint` is set correctly
- [ ] `destructiveHint` is set correctly
- [ ] `idempotentHint` is set correctly
- [ ] `openWorldHint` is set to `True` (all tools make HTTP requests)
- [ ] Tool docstring clearly describes what it does
- [ ] Tool parameters have type hints and descriptions
- [ ] Error handling follows existing patterns (`_handle_error`)

## Screenshots / Logs

<!-- If applicable, add screenshots or log output showing the change working. -->

## Additional Notes

<!-- Any additional information that reviewers should know. -->
