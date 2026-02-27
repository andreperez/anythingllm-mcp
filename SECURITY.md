# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in AnythingLLM MCP Server, please report it responsibly.

### How to Report

1. **Do NOT open a public issue** for security vulnerabilities.
2. Send an email to the maintainer with the subject line: `[SECURITY] anythingllm-mcp vulnerability report`.
3. Alternatively, use [GitHub's private vulnerability reporting](https://github.com/andreperez/anythingllm-mcp/security/advisories/new).

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

| Action                     | Timeframe       |
| -------------------------- | --------------- |
| Acknowledgment of report   | Within 48 hours |
| Initial assessment         | Within 5 days   |
| Fix development & release  | Within 30 days  |

### What to Expect

- You will receive an acknowledgment confirming receipt of your report.
- We will work with you to understand and validate the issue.
- A fix will be developed and tested before public disclosure.
- You will be credited in the release notes (unless you prefer anonymity).

## Security Best Practices for Users

### API Key Management

- **Never hardcode** your AnythingLLM API key in source code.
- Store the API key in environment variables or a `.env` file.
- Ensure `.env` is listed in `.gitignore` (it is by default in this project).
- Rotate your API key periodically.

```bash
# Good: Use environment variables
export ANYTHINGLLM_API_KEY="your-key-here"

# Bad: Never commit keys to version control
ANYTHINGLLM_API_KEY="sk-..." # DO NOT do this in code
```

### Network Security

- Run AnythingLLM on `localhost` or within a trusted network when possible.
- If exposing AnythingLLM externally, use HTTPS and a reverse proxy.
- The MCP server communicates with AnythingLLM via HTTP — ensure the connection is secured in production environments.

### Dependency Security

- Regularly update dependencies: `uv sync --upgrade`
- Check for known vulnerabilities: `uv pip audit` or use GitHub's Dependabot alerts.

## Scope

This security policy covers:

- The `anythingllm-mcp` Python package
- The MCP server implementation (`anythingllm_mcp.py`)
- Configuration and deployment files

This policy does **not** cover:

- AnythingLLM itself (report at [AnythingLLM's repository](https://github.com/Mintplex-Labs/anything-llm))
- Third-party dependencies (report to their respective maintainers)
- MCP protocol specification (report at [MCP's repository](https://github.com/modelcontextprotocol/specification))
