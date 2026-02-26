# AnythingLLM MCP Server

MCP server for [AnythingLLM](https://anythingllm.com) with tools for:

- Workspace management
- Chat and thread operations
- Document operations and embeddings
- Vector search
- System and model inspection

## Requirements

- Python 3.10+
- `uv` installed
- AnythingLLM running and reachable
- Valid AnythingLLM API key

## Installation

```powershell
git clone https://github.com/andreperez/anythingllm-mcp.git
cd anythingllm-mcp
uv sync
```

## Configuration

Set environment variables before running:

```powershell
$env:ANYTHINGLLM_BASE_URL = "http://localhost:3001"
$env:ANYTHINGLLM_API_KEY = "your_api_key_here"
```

You can copy `.env.example` and load it with your preferred tooling.

## Client setup

Replace `/path/to/anythingllm-mcp` below with the **absolute path** where you cloned the repository.

### VS Code

Add to your user or workspace `mcp.json` (Command Palette → "MCP: Open User Configuration"):

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

Add to `.cursor/mcp.json` in your project root (or global config):

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

> **Note:** `ANYTHINGLLM_BASE_URL` defaults to `http://localhost:3001`. Change it if your instance runs on a different address or port.

## Run (standalone)

```powershell
uv run anythingllm-mcp
```

## Development

```powershell
uv sync --extra dev
uv run pytest
```

## Security notes

- Never commit real API keys.
- Use environment variables for secrets.
- Use least-privileged AnythingLLM API tokens when possible.

## License

MIT
