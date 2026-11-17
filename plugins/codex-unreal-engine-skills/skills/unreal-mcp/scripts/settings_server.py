"""Expose the Unreal endpoint as native plugin settings via openai/settings.

This local stdio server works independently of the Unreal Editor connection.
Only JSON-RPC is written to stdout. No third-party Python packages are required.
"""

import json
import ipaddress
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

sys.dont_write_bytecode = True

from configure_endpoint import codex_cli, effective_server, endpoint, save_url


VERSION = "0.1.6"
READ_TOOL = "read_settings"
UPDATE_TOOL = "update_settings"
RESET_TOOL = "reset_defaults"
EXTENSION = {"openai/settings": {"readTool": READ_TOOL, "updateTool": UPDATE_TOOL}}
DEFAULTS = {"ip": "127.0.0.1", "path": "/mcp", "port": 8000}
DEFAULT_URL = "http://127.0.0.1:8000/mcp"
FIELD_SCHEMAS = {
    "ip": {
        "type": "string", "title": "IP",
        "description": "默认 127.0.0.1（本机）。支持 IPv4、IPv6 或主机名；不要填写 http://、路径或端口。",
        "minLength": 1, "maxLength": 253,
    },
    "path": {
        "type": "string", "title": "URL 路径",
        "description": "默认 /mcp。以 / 开头，与 UE 的服务器 URL 路径一致；不要填写完整地址或查询参数。",
        "minLength": 1, "pattern": r"^/(?!/)[^\s?#\\]*$",
    },
    "port": {
        "type": "integer", "title": "端口号",
        "description": "默认 8000。范围 1–65535，与 UE 的服务器端口号一致。按 Enter 或移开焦点保存。",
        "minimum": 1, "maximum": 65535,
    },
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
                "type": "object", "properties": FIELD_SCHEMAS,
                "minProperties": 1, "additionalProperties": False,
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
    {
        "name": RESET_TOOL,
        "title": "恢复默认值",
        "description": "Restore the Unreal MCP client address to http://127.0.0.1:8000/mcp when the user clicks Restore defaults.",
        "inputSchema": {"type": "object", "additionalProperties": False},
        "outputSchema": {
            "type": "object", "properties": {"values": {"type": "object"}},
            "required": ["values"],
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False,
                        "idempotentHint": True, "openWorldHint": False},
    },
]


def validated_fields(fields):
    ip, path, port = fields["ip"], fields["path"], fields["port"]
    if not isinstance(ip, str) or not ip or len(ip) > 253 or "%" in ip:
        raise ValueError("IP 无效，请填写 IP 或主机名，例如 127.0.0.1。")
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        # Preserve existing DNS endpoints, but reject malformed numeric IPs,
        # embedded schemes, ports, credentials and paths.
        if (re.fullmatch(r"[0-9.]+", ip) or not all(
                re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
                for label in ip.removesuffix(".").split("."))):
            raise ValueError("IP 无效：不要包含协议、端口或路径。IPv6 不需要方括号。")
    if (not isinstance(path, str) or not re.fullmatch(FIELD_SCHEMAS["path"]["pattern"], path)
            or any(ord(c) < 32 or ord(c) == 127 for c in path)
            or re.search(r"%(?![0-9A-Fa-f]{2})", path)):
        raise ValueError("URL 路径须以 / 开头，不能包含空格、查询参数、片段或无效转义。例如 /mcp。")
    if (isinstance(port, bool) or not isinstance(port, (int, float))
            or not 1 <= port <= 65535 or int(port) != port):
        raise ValueError("端口号必须是 1–65535 的整数，默认 8000。")
    return {"ip": ip, "path": path, "port": int(port)}


def split_endpoint(raw):
    parsed = urlsplit(endpoint(raw))
    fields = validated_fields({
        "ip": parsed.hostname, "path": parsed.path or "/",
        "port": parsed.port or (443 if parsed.scheme == "https" else 80),
    })
    return parsed.scheme, fields


def combine_endpoint(scheme, fields):
    fields = validated_fields(fields)
    host = f'[{fields["ip"]}]' if ":" in fields["ip"] else fields["ip"]
    return endpoint(f'{scheme}://{host}:{fields["port"]}{fields["path"]}')


def write_endpoint(cli, url, previous):
    if previous != url:
        save_url(cli, url, expected_url=previous)
    raw = effective_server(cli)["transport"]["url"]
    if raw != url:
        raise ValueError("项目或管理配置覆盖了此地址，请检查对应设置。")
    return split_endpoint(raw)[1]


def call_tool(params):
    try:
        name = params.get("name")
        args = params.get("arguments", {})
        if name == READ_TOOL:
            if args != {}:
                raise ValueError("read_settings takes no arguments.")
            raw = effective_server(codex_cli())["transport"]["url"]
            try:
                scheme, fields = split_endpoint(raw)
                note = f"当前使用 {scheme.upper()}；修改后重新连接 MCP 或新开本地会话。"
            except ValueError:
                # Keep the recovery button available without silently writing
                # defaults just because the user opened the page.
                fields = dict(DEFAULTS)
                note = "当前地址格式无效，暂显示默认值；点击恢复默认值后才会修复已保存地址。"
            data = {
                "schema": {"type": "object", "properties": FIELD_SCHEMAS},
                "values": fields,
                "layout": [{"kind": "group", "title": "Unreal Editor 连接",
                            "items": [{"kind": "property", "property": key} for key in DEFAULTS]
                            + [{"kind": "tool", "tool": RESET_TOOL,
                                "description": "恢复为 127.0.0.1、/mcp、8000（HTTP）并保存；点击后重新打开此页刷新显示。" + note}]}],
            }
        elif name == UPDATE_TOOL:
            if (not isinstance(args, dict) or set(args) != {"set"}
                    or not isinstance(args["set"], dict) or not args["set"]
                    or not set(args["set"]) <= set(DEFAULTS)):
                raise ValueError("仅支持修改 IP、URL 路径和端口号。")
            cli = codex_cli()
            previous = effective_server(cli)["transport"]["url"]
            scheme, fields = split_endpoint(previous)
            url = combine_endpoint(scheme, {**fields, **args["set"]})
            data = {"values": write_endpoint(cli, url, previous)}
        elif name == RESET_TOOL:
            if args != {}:
                raise ValueError("恢复默认值不接受参数。")
            cli = codex_cli()
            previous = effective_server(cli)["transport"]["url"]
            data = {"values": write_endpoint(cli, DEFAULT_URL, previous)}
            return {"content": [{"type": "text", "text": "已恢复默认值：127.0.0.1 / /mcp / 8000。重新打开插件页查看；重新连接 MCP 或新开本地会话后使用。"}],
                    "structuredContent": data}
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
