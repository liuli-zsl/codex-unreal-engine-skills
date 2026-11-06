"""Configure the installed Unreal MCP connection through Codex's user settings."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from threading import Timer
from urllib.parse import urlsplit


SERVER = "unreal-mcp"


def endpoint(value):
    try:
        url = urlsplit(value)
        valid = (
            url.scheme in ("http", "https")
            and url.hostname
            and url.port != 0
            and url.username is None
            and not any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value)
            and not any(c in value for c in ("\\", "#", "?"))
        )
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("Enter a full HTTP(S) MCP URL without credentials, a query or a fragment.")
    return value


def parent_codex_cli():
    # MCP children receive a filtered environment. Prefer the app-server that
    # launched this server over an unrelated (possibly older) CLI on PATH.
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD,
                                                     wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, os.getppid())
        if not handle:
            return None
        try:
            size = wintypes.DWORD(32768)
            buffer = ctypes.create_unicode_buffer(size.value)
            if not kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
                return None
            path = buffer.value
        finally:
            kernel.CloseHandle(handle)
    elif sys.platform.startswith("linux"):
        try:
            path = os.readlink(f"/proc/{os.getppid()}/exe")
        except OSError:
            return None
    else:
        return None
    return path if Path(path).stem.lower() == "codex" else None


def codex_cli():
    cli = os.environ.get("CODEX_APP_RUNTIME_CLI_PATH") or parent_codex_cli() or shutil.which("codex")
    if not cli:
        raise ValueError("Open a local Codex session or install the Codex CLI.")
    return cli


def effective_server(cli):
    result = subprocess.run(
        [cli, "mcp", "get", SERVER, "--json"], capture_output=True, text=True,
        encoding="utf-8", timeout=20,
    )
    if result.returncode:
        raise ValueError("Codex could not read unreal-mcp. Check that the plugin is enabled.")
    server = json.loads(result.stdout)
    if server["transport"]["type"] != "streamable_http":
        raise ValueError("An existing unreal-mcp connection uses a different transport.")
    return server


def rpc(process, number, method, params):
    message = {"id": number, "method": method, "params": params}
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()
    for line in process.stdout:
        response = json.loads(line)
        if response.get("id") == number:
            if "error" in response:
                raise ValueError(f"Codex rejected {method}: {response['error']['message']}")
            return response["result"]
    raise ValueError(f"Codex stopped or timed out during {method}. Check the effective URL.")


def save_url(cli, url, expected_url=None):
    # Use Codex's TOML editor to preserve comments, other keys and concurrent edits.
    with subprocess.Popen(
        [cli, "app-server", "--listen", "stdio://"], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
    ) as process:
        timer = Timer(25, process.kill)
        timer.start()
        try:
            rpc(process, 1, "initialize", {"clientInfo": {"name": "unreal-endpoint", "version": "1"}})
            process.stdin.write('{"method":"initialized"}\n')
            process.stdin.flush()
            config = rpc(process, 2, "config/read", {"includeLayers": True, "cwd": os.getcwd()})
            user = next((layer for layer in config["layers"] if
                         layer["name"]["type"] == "user" and not layer["name"].get("profile")), None)
            if user is None:
                raise ValueError("Codex did not expose its writable user settings.")
            if expected_url is not None and effective_server(cli)["transport"]["url"] != expected_url:
                raise ValueError("The address changed concurrently. Refresh settings and try again.")
            for settings in (user["config"], config["config"]):
                existing = settings.get("mcp_servers", {}).get(SERVER, {})
                if "command" in existing:
                    raise ValueError("A configured unreal-mcp uses stdio. Review it in MCP settings.")
                credential_keys = {"bearer_token_env_var", "http_headers", "env_http_headers",
                                   "http_headers_helper"}
                if any(value for key, value in existing.items()
                       if key in credential_keys or key.startswith("oauth")):
                    raise ValueError("This connection has authentication or headers. "
                                     "Review it in MCP settings before changing the destination.")
            path = Path(user["name"]["file"])
            if path.is_file():
                with tempfile.NamedTemporaryFile(prefix=path.name + ".bak-unreal-", dir=path.parent,
                                                 delete=False) as backup:
                    with path.open("rb") as original:
                        shutil.copyfileobj(original, backup)
                print("Backup:", backup.name, file=sys.stderr)
            write = rpc(process, 3, "config/value/write", {
                "filePath": str(path), "expectedVersion": user["version"],
                "keyPath": f"mcp_servers.{SERVER}.url", "value": url, "mergeStrategy": "replace",
            })
            if write.get("overriddenMetadata"):
                print("A higher-priority Codex setting overrides this user preference.", file=sys.stderr)
        finally:
            try:
                process.stdin.close()
                process.wait(timeout=3)
            except (BrokenPipeError, subprocess.TimeoutExpired):
                process.kill()
            finally:
                timer.cancel()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", dest="new_url", metavar="URL",
                        help="Save this endpoint. With no arguments, show the effective endpoint.")
    args = parser.parse_args()
    url = endpoint(args.new_url) if args.new_url is not None else None
    cli = codex_cli()
    server = effective_server(cli)
    if url and url != server["transport"]["url"]:
        save_url(cli, url)
        server = effective_server(cli)
        if server["transport"]["url"] != url:
            raise ValueError("User settings were written, but the effective URL differs. Check project or managed settings.")
    current = server["transport"]["url"]
    try:
        print("Effective URL:", endpoint(current))
    except ValueError:
        print("Effective URL: hidden (inspect this URL in MCP settings).")
    print("Enabled:", server["enabled"])


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        sys.exit(str(exc))
