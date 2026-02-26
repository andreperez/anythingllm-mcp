# Release Checklist

## 0) Before first release

- [ ] Update URLs in `pyproject.toml` (`project.urls`) with your real GitHub repository URL.
- [ ] Confirm package name availability on PyPI (`anythingllm-mcp`).
- [ ] Ensure no secrets are committed (`.env`, API keys).
- [ ] Confirm tests pass locally.
- [ ] Confirm package builds (`sdist` and `wheel`).

## 1) Initialize Git repository (first time only)

```powershell
# run from repository root
git init
git add .
git commit -m "feat: initial release-ready MCP server"
```

## 2) Create GitHub repository and push

```powershell
# run from repository root
gh repo create andreperez/anythingllm-mcp --public --source . --remote origin --push
```

If you already created the repo on GitHub:

```powershell
git remote add origin https://github.com/andreperez/anythingllm-mcp.git
git branch -M main
git push -u origin main
```

## 3) Validate project

```powershell
# run from repository root
uv sync --extra dev
uv run pytest
uv build
```

## 4) Publish to TestPyPI first (recommended)

```powershell
# run from repository root
uv publish --index testpypi
```

Validate installation from TestPyPI in a clean environment:

```powershell
uv tool install --index https://test.pypi.org/simple anythingllm-mcp
```

## 5) Publish to PyPI

```powershell
# run from repository root
uv publish
```

## 6) Create git tag and GitHub Release

```powershell
# run from repository root
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
```

Create release notes from changelog:

```powershell
gh release create v1.0.0 --title "v1.0.0" --notes-file CHANGELOG.md
```

## 7) Post-release checks

- [ ] Verify package page on PyPI.
- [ ] Verify `uv tool install anythingllm-mcp` works from PyPI.
- [ ] Verify README installation and env configuration instructions are correct.
- [ ] Verify CI passing on default branch.

## Notes on MCP directories

- There is no universal official MCP package registry used by every client.
- Standard distribution remains: GitHub repository + PyPI package.
- You can additionally submit the project to client/community directories when available.

## Privacy guardrails

- Never commit your VS Code user profile MCP config file (`.../Code/User/.../mcp.json`).
- Keep real API keys only in environment variables or secret stores.
