# pyenv-manager-mcp

An MCP server for managing Python versions via [pyenv](https://github.com/pyenv/pyenv).

## Requirements

- Linux or macOS (or Windows via WSL)
- [pyenv](https://github.com/pyenv/pyenv) installed and available on `PATH`
- [uv](https://docs.astral.sh/uv/)

## Installation

### Linux / macOS

Add to your MCP config:

```json
{
  "mcpServers": {
    "pyenv-manager": {
      "command": "uv",
      "args": ["--directory", "/path/to/pyenv-manager-mcp", "run", "pyenv-manager-mcp"]
    }
  }
}
```

### Windows (via WSL)

```json
{
  "mcpServers": {
    "pyenv-manager": {
      "command": "wsl.exe",
      "args": [
        "bash",
        "-c",
        "export PATH=/home/<user>/.pyenv/bin:/home/<user>/.pyenv/shims:/home/<user>/.local/bin:/usr/local/bin:/usr/bin:/bin && cd /mnt/c/path/to/pyenv-manager-mcp && uv run pyenv-manager-mcp"
      ]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `list_versions` | List installed Python versions |
| `get_current_version` | Get the currently active Python version |
| `list_available_downloads` | List versions available to install (supports optional `filter`, e.g. `"3.12"`) |
| `install_version` | Install a specific Python version |
| `set_global_version` | Set the global Python version |
| `set_local_version` | Set the local (directory) Python version |
