"""Expose the Unreal endpoint as native plugin settings via openai/settings.

This local stdio server works independently of the Unreal Editor connection.
Only JSON-RPC is written to stdout. No third-party Python packages are required.
"""

import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

from configure_endpoint import codex_cli, effective_server, endpoint, save_url


VERSION = "0.1.4"
READ_TOOL = "read_settings"
UPDATE_TOOL = "update_settings"
EXTENSION = {"openai/settings": {"readTool": READ_TOOL, "updateTool": UPDATE_TOOL}}
URL_SCHEMA = {
    "type": "string",
    "title": "Unreal MCP 地址",
    "description": "输入 UE 编辑器的完整 HTTP(S) 地址。按 Enter 或离开输入框保存；保存后重新连接 MCP 或新开本地会话。",
    "minLength": 1,
}
TOOLS = [
    {
        "name": READ_TOOL,
        "title": "读取 Unreal MCP 地址",
        "description": "Read the effective Unreal MCP URL for the plugin settings page.",
        "inputSchema": {"type": "object", "additionalProperties": False},
        "outputSchema": {
            "type": "object",
            "properties": {"schema": {"type": "object"}, "values": {"type": "object"},
                           "layout": {"type": "array", "items": {"type": "object"}}},
            "required": ["schema", "values"],
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": UPDATE_TOOL,
        "title": "保存 Unreal MCP 地址",
        "description": "Save the URL explicitly entered in the plugin settings page to Codex user settings.",
        "inputSchema": {
            "type": "object",
            "properties": {"set": {
                "type": "object", "properties": {"url": {"type": "string"}},
                "required": ["url"], "additionalProperties": False,
            }},
            "required": ["set"], "additionalProperties": False,
        },
        "outputSchema": {
            "type": "object", "properties": {"values": {"type": "object"}},
            "required": ["values"],
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False,
                        "idempotentHint": True, "openWorldHint": False},
    },
]


def values(cli):
    # Never expose a URL containing embedded credentials to the settings UI.
    return {"url": endpoint(effective_server(cli)["transport"]["url"])}


def call_tool(params):
    try:
        name = params.get("name")
        args = params.get("arguments", {})
        if name == READ_TOOL:
            if args != {}:
                raise ValueError("read_settings takes no arguments.")
            data = {
                "schema": {"type": "object", "properties": {"url": URL_SCHEMA}},
                "values": values(codex_cli()),
                "layout": [{"kind": "group", "title": "Unreal Editor 连接",
                            "items": [{"kind": "property", "property": "url"}]}],
            }
        elif name == UPDATE_TOOL:
            if (not isinstance(args, dict) or set(args) != {"set"}
                    or not isinstance(args["set"], dict) or set(args["set"]) != {"url"}
                    or not isinstance(args["set"]["url"], str)):
                raise ValueError("update_settings requires set.url as a string.")
            url = endpoint(args["set"]["url"])
            cli = codex_cli()
            if values(cli)["url"] != url:
                save_url(cli, url)
            current = values(cli)
            if current["url"] != url:
                raise ValueError("A project or managed setting overrides this user URL.")
            data = {"values": current}
        else:
            raise ValueError("Unknown settings tool.")
        return {"content": [], "structuredContent": data}
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        return {"isError": True, "content": [{"type": "text", "text": str(exc)}]}


def dispatch(request):
    method = request.get("method")
    params = request.get("params") or {}
    if not isinstance(params, dict):
        return {"error": {"code": -32602, "message": "Expected object params."}}
    if method == "initialize":
        return {"result": {
            "protocolVersion": "2025-11-25",
            "serverInfo": {"name": "unreal-mcp-settings", "version": VERSION,
                           "title": "Unreal MCP 地址设置"},
            "capabilities": {"tools": {}, "experimental": EXTENSION},
        }}
    if method == "tools/list":
        return {"result": {"tools": TOOLS}}
    if method == "tools/call":
        return {"result": call_tool(params)}
    if method == "ping":
        return {"result": {}}
    return {"error": {"code": -32601, "message": "Method not found."}}


def main():
    # Codex filters CODEX_HOME from MCP child environments. Recover only the
    # documented-on-this-host installed cache layout, never guess a different
    # user's default home. This also keeps isolated test profiles isolated.
    if "CODEX_HOME" not in os.environ:
        root = Path(os.environ.get("PLUGIN_ROOT", "")).resolve()
        if (len(root.parents) < 5 or root.parents[2].name != "cache"
                or root.parents[3].name != "plugins"):
            sys.exit("Cannot determine this plugin's Codex profile from PLUGIN_ROOT.")
        os.environ["CODEX_HOME"] = str(root.parents[4])
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    for line in sys.stdin:
        try:
            request = json.loads(line)
        except ValueError:
            response = {"id": None, "error": {"code": -32700, "message": "Parse error."}}
        else:
            if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
                response = {"id": None, "error": {"code": -32600, "message": "Invalid request."}}
            elif "id" not in request:
                continue
            else:
                response = {"id": request["id"], **dispatch(request)}
        print(json.dumps({"jsonrpc": "2.0", **response}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
