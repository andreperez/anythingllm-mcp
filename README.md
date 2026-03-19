# AnythingLLM MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that
lets MCP-compatible clients (VS Code, Claude Desktop, Cursor, and others)
interact with [AnythingLLM](https://anythingllm.com). Available tools:

- Workspace management
- Chat and thread operations
- Document operations and embeddings
- Vector search
- System and model inspection

## Requirements

- **Python 3.10+** — verify: `python --version` or `python3 --version`.
  [Download](https://www.python.org/downloads/) if not installed.
- **uv** (Python package manager) — verify: `uv --version`.
  [Install instructions](https://docs.astral.sh/uv/getting-started/installation/).
- **AnythingLLM running and reachable** — open `http://localhost:3001` in a
  browser to confirm. If it runs in Docker, make sure the port is published
  (e.g., `-p 3001:3001`).
- **AnythingLLM API key** — create one in the AnythingLLM web interface (look
  for **API Keys** or **Developer API** in Settings). Copy the key and store it
  securely; it is shown only once.

## Installation

```sh
git clone https://github.com/andreperez/anythingllm-mcp.git
cd anythingllm-mcp
uv sync
```

`uv sync` reads `pyproject.toml` and installs all required dependencies into a
local virtual environment. You do not need to create or activate the environment
manually — `uv run` handles that automatically.

## Configuration

The server reads configuration from these environment variables at startup:

- `ANYTHINGLLM_BASE_URL`: Base URL of your AnythingLLM instance.
  Defaults to `http://localhost:3001` if not set.
- `ANYTHINGLLM_API_KEY`: API key for authenticating with AnythingLLM.
  This value is required.

The server does **not** load `.env` files by itself. You must either:

- Set the variables in the shell before starting the server.
- Use a tool that loads `.env` files for you.
- Pass the variables directly in your MCP client configuration.

### Option 1: Set variables in your current shell

PowerShell:

```powershell
$env:ANYTHINGLLM_BASE_URL = "http://localhost:3001"
$env:ANYTHINGLLM_API_KEY = "your_api_key_here"
```

Bash:

```bash
export ANYTHINGLLM_BASE_URL="http://localhost:3001"
export ANYTHINGLLM_API_KEY="your_api_key_here"
```

Command Prompt (`cmd.exe`):

```bat
set ANYTHINGLLM_BASE_URL=http://localhost:3001
set ANYTHINGLLM_API_KEY=your_api_key_here
```

Use the host-exposed URL for your deployment. For Docker port mappings like
`3002:3001`, set `ANYTHINGLLM_BASE_URL` to `http://localhost:3002` because the
MCP server connects from the host, not from inside the container.

### Option 2: Use a `.env` file with `uv`

Copy the example file:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Bash:

```bash
cp .env.example .env
```

Command Prompt (`cmd.exe`):

```bat
copy .env.example .env
```

Edit `.env` so it contains your real values:

```dotenv
ANYTHINGLLM_BASE_URL=http://localhost:3001
ANYTHINGLLM_API_KEY=replace_with_your_real_api_key
```

Then start the server with:

```sh
uv run --env-file .env anythingllm-mcp
```

This tells `uv` to load variables from `.env` before starting the server.

### Option 3: Pass variables in your MCP client configuration

Most MCP clients accept an `env` block in their configuration file (see the
[Client setup](#client-setup) examples below). When the `env` block contains
`ANYTHINGLLM_API_KEY` and `ANYTHINGLLM_BASE_URL`, you do not need to export
variables in the shell or use a `.env` file.

## Client setup

Replace `/path/to/anythingllm-mcp` in the examples below with the **absolute
path** where you cloned the repository. Examples:

- Linux / macOS: `/home/youruser/anythingllm-mcp`
- Windows: `C:\\Users\\youruser\\anythingllm-mcp` (use double backslashes `\\`
  inside JSON strings)

### VS Code

Add to your user or workspace `mcp.json`. Open the Command Palette
(`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS) and run
**MCP: Open User Configuration**:

```json
{
  "servers": {
    "anythingllm": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/anythingllm-mcp",
        "anythingllm-mcp"
      ],
      "env": {
        "ANYTHINGLLM_API_KEY": "${input:anythingllm_api_key}",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
      }
    }
  }
}
```

> VS Code supports `${input:name}` to prompt for the API key on each session.
>
> In a multi-root workspace, prefer an absolute path for `--directory` if the
> MCP server lives outside the current folder root.

If VS Code shows only a partial tool list after you update the server or switch
from another AnythingLLM integration to this local one:

1. Run `MCP: List Servers` and confirm `anythingllm` or your chosen server name
  starts successfully.
2. Run `MCP: Reset Cached Tools` to clear stale tool metadata.
3. Restart the MCP server from `MCP: List Servers`.

### Claude Desktop

Edit `claude_desktop_config.json` (Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "anythingllm": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/anythingllm-mcp",
        "anythingllm-mcp"
      ],
      "env": {
        "ANYTHINGLLM_API_KEY": "YOUR_API_KEY",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project root, or to the global config at
`~/.cursor/mcp.json` (Linux/macOS) / `%USERPROFILE%\.cursor\mcp.json` (Windows):

```json
{
  "mcpServers": {
    "anythingllm": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/anythingllm-mcp",
        "anythingllm-mcp"
      ],
      "env": {
        "ANYTHINGLLM_API_KEY": "YOUR_API_KEY",
        "ANYTHINGLLM_BASE_URL": "http://localhost:3001"
      }
    }
  }
}
```

> **Note:** `ANYTHINGLLM_BASE_URL` defaults to `http://localhost:3001`, which is
> the application port inside the container. If you publish Docker as
> `3002:3001`, use `http://localhost:3002` in client configuration.

## Run (standalone)

If you already exported the variables in your shell:

```sh
uv run anythingllm-mcp
```

If you want to load them from `.env` at launch time:

```sh
uv run --env-file .env anythingllm-mcp
```

## Development

Install test dependencies and run the test suite:

```sh
uv sync --extra dev
uv run pytest
```

## Troubleshooting

### "API key is missing" or 401 Unauthorized

The server could not authenticate with AnythingLLM. Check that:

1. `ANYTHINGLLM_API_KEY` is set in your environment or in the `env` block of
   your MCP client configuration.
2. The key matches an active key in AnythingLLM (Settings → API Keys).
3. The key has no leading or trailing whitespace.

### "Connection refused" or timeout

The server could not reach AnythingLLM. Check that:

1. AnythingLLM is running (open `http://localhost:3001` in a browser).
2. `ANYTHINGLLM_BASE_URL` points to the correct host and port.
3. No firewall or VPN is blocking the connection.

### Docker port mismatch

If AnythingLLM runs in Docker with a port mapping like `3002:3001`:

- **Inside the container**, the application listens on port `3001`.
- **On the host**, you access it on port `3002`.

Because the MCP server runs on the host (not inside the container), set:

```dotenv
ANYTHINGLLM_BASE_URL=http://localhost:3002
```

Always use the **host port** (the left side of the `-p` or `ports:` mapping).

### MCP server running inside a container (Dev Containers, Docker Compose)

If the MCP server itself runs inside a container (for example, a
[VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)),
`localhost` refers to that container's own network — not to the host machine.
To reach AnythingLLM running on the host or in another container with a
published port, use `host.docker.internal`:

```dotenv
ANYTHINGLLM_BASE_URL=http://host.docker.internal:3001
```

If both the MCP server and AnythingLLM are containers on the **same Docker
network** (for example, in the same `docker-compose.yml`), use the **service
name** as hostname instead:

```dotenv
# "anythingllm" is the service name defined in docker-compose.yml
ANYTHINGLLM_BASE_URL=http://anythingllm:3001
```

In this case, use the **container port** (`3001`), not the host-published port.

> `host.docker.internal` is supported on Docker Desktop (Windows and macOS) and
> on Docker Engine 20.10+ for Linux (requires `--add-host=host.docker.internal:host-gateway`
> or the equivalent `extra_hosts` in Compose).

## Security notes

- Never commit real API keys.
- Use environment variables for secrets.
- Use least-privileged AnythingLLM API tokens when possible.

## License

MIT
