import asyncio
import shutil
from mcp.server.mcpserver import MCPServer

# Initialize MCP Server
mcp = MCPServer("pyenv-manager")


def _check_pyenv_installed() -> str | None:
    """Check if pyenv executable is available in PATH."""
    if not shutil.which("pyenv"):
        return (
            "Error: 'pyenv' is not installed or not available in system PATH. "
            "Please ensure pyenv is installed and correctly configured."
        )
    return None


async def _run_pyenv_command(*args: str) -> str:
    """Execute a pyenv subcommand asynchronously."""
    error_msg = _check_pyenv_installed()
    if error_msg:
        return error_msg

    try:
        proc = await asyncio.create_subprocess_exec(
            "pyenv",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        output = stdout.decode().strip()
        errors = stderr.decode().strip()

        if proc.returncode != 0:
            return f"Error (exit code {proc.returncode}):\n{errors or output}"

        return output if output else "Command executed successfully with no output."
    except Exception as e:
        return f"Execution error: {str(e)}"


@mcp.tool()
async def list_versions() -> str:
    """List all Python versions installed locally via pyenv."""
    return await _run_pyenv_command("versions")


@mcp.tool()
async def get_current_version() -> str:
    """Get the currently active Python version (pyenv version)."""
    return await _run_pyenv_command("version")


@mcp.tool()
async def list_available_downloads(filter: str = "") -> str:
    """List all Python versions available for installation via pyenv.

    Args:
        filter: Optional string to filter versions (e.g., '3.12' to show only 3.12.x versions).
    """
    output = await _run_pyenv_command("install", "--list")
    if filter:
        lines = [line for line in output.splitlines() if filter in line]
        return "\n".join(lines) if lines else f"No versions found matching '{filter}'."
    return output


@mcp.tool()
async def install_version(version: str) -> str:
    """Install a specific Python version using pyenv.

    Args:
        version: The exact version string to install (e.g., '3.12.2').
    """
    return await _run_pyenv_command("install", version)


@mcp.tool()
async def set_global_version(version: str) -> str:
    """Set the global Python version for pyenv.

    Args:
        version: The version string to set globally (e.g., '3.12.2').
    """
    return await _run_pyenv_command("global", version)


@mcp.tool()
async def set_local_version(version: str) -> str:
    """Set the local directory Python version (.python-version).

    Args:
        version: The version string to set locally (e.g., '3.12.2').
    """
    return await _run_pyenv_command("local", version)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
