# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-25

### Added
- MCP tools for AnythingLLM workspaces, chat, threads, documents, search, and system operations.
- Release documentation: `README.md`, `PUBLISHING.md`, and `RELEASE_CHECKLIST.md`.
- Environment template file: `.env.example`.
- CI workflow for tests.
- Basic test suite for authentication, validation, and timeout handling.

### Changed
- Strengthened API and error handling paths.
- Added input validation for numeric ranges and chat mode typing.
- Added explicit `main()` entrypoint for package script execution.
- Enhanced `pyproject.toml` metadata for publication.

### Security
- Enforced API key presence before API calls.
- Added guidance to avoid committing secrets.
