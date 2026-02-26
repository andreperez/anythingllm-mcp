# Publishing Guide

This project can be published and distributed in multiple channels.

## 1) Official Python package index (PyPI)

Yes, this MCP server can be published to PyPI.

### Prerequisites

- A PyPI account
- API token from PyPI
- Project metadata configured in `pyproject.toml`

### Build and publish

```powershell
cd AnythingLLM/mcp-server
uv build
uv publish
```

For safer first release, publish to TestPyPI first.

## 2) `uv` distribution

`uv` does not have a separate public registry. It installs from package indexes (PyPI by default).

So once published to PyPI, users can install with:

```powershell
uv tool install anythingllm-mcp
```

or add as dependency:

```powershell
uv add anythingllm-mcp
```

## 3) MCP ecosystem directories / catalogs

There is currently no single universal official MCP package registry used by all clients.

Common approach:

- Publish source on GitHub
- Publish package on PyPI
- Add your project to client/community directories when available

Because each directory has its own onboarding process, treat those as optional distribution channels on top of GitHub + PyPI.

## 4) Recommended release flow

1. Run CI and tests
2. Tag version in Git
3. Build with `uv build`
4. Publish to TestPyPI
5. Validate install via `uv tool install --index https://test.pypi.org/simple anythingllm-mcp`
6. Publish to PyPI
7. Create GitHub Release notes

## 5) Practical checklist

- [ ] `README.md` has installation and configuration instructions
- [ ] `.env.example` present
- [ ] `LICENSE` present
- [ ] CI green
- [ ] No secrets in repository
- [ ] `project.urls` in `pyproject.toml` updated with real GitHub URL
