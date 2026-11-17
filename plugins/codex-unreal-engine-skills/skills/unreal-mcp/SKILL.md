---
name: unreal-mcp
description: "Inspect or change a live Unreal Editor through Epic's official MCP. Use for actual editor or asset tasks and connection diagnosis; skip conceptual Unreal questions that need no project access."
---

# Unreal MCP for Codex

Use Epic's official Unreal MCP server and discover its live schemas. This package
changes the client integration, not the Unreal tool implementations.

## Configure the connection from the plugin page

The plugin's native settings form uses the `openai/settings` MCP extension.
Direct users to the plugin details page > Settings > Unreal Editor 连接.
The **IP**, **URL 路径** and **端口号** fields default to `127.0.0.1`, `/mcp`
and `8000`. Press Enter or leave a field to save only that field. Invalid values
are rejected. **恢复默认值** restores and saves the default HTTP endpoint; reopen
the page to refresh the displayed fields. Do not replace this UI with a chat
prompt or silently invoke reset. Existing custom URLs and HTTPS survive ordinary
edits and upgrades.

The bundled [settings server](scripts/settings_server.py) reads the effective
address and uses the [endpoint helper](scripts/configure_endpoint.py) to back up
and update only the user's `mcp_servers.unreal-mcp.url`. It works while Unreal
is offline. It requires Python 3 and a desktop host supporting structured MCP
settings. Reconnect MCP or start a new local chat after saving. The Unreal
Editor's listening address is configured separately. Report unsupported hosts
or write errors honestly; do not rewrite the plugin cache to force a value.

## Desktop operating contract

- Explicit user instructions and authorization boundaries take precedence over
  this skill. An analysis request does not authorize project edits.
- Use a conversation running on This computer / Local. A cloud executor's
  loopback address is not the user's Unreal Editor.
- Prefer the already available Unreal connection. Plugin tools may be namespaced;
  discover the actual tool handles rather than guessing their names.
- Resolve the endpoint from the user's existing working connection and intended
  Unreal Editor configuration/logs. Preserve a custom port and URL path.
- The bundled `http://127.0.0.1:8000/mcp` is the official first-setup default,
  not a detected endpoint. Never overwrite an existing configuration with it.
- Do not rewrite global client configuration, restart the editor, change
  permissions, or install a proxy merely because a tool is not visible.

## Discover, then dispatch

Inspect the connected server's advertised tools. Use `list_toolsets` when you
need to find the toolset. Follow the route the server offers:

| Advertised tools | How to obtain the schema |
| --- | --- |
| `describe_toolset` (UE 5.8) | Pass the exact toolset name in `toolset_name`. Read the selected tool's schema. |
| `describe_toolsets` and `describe_tools` (UE 5.9 Preview) | List tools with `toolset_names` (an array). For a known tool, pass its qualified name in the `tool_names` array to `describe_tools`. To fetch schemas for a whole toolset, pass `include_schemas: true` to `describe_toolsets`. |
| Domain tool exposed directly (tool search disabled) | Read its advertised schema and call its native handle directly. |

In tool-search mode, use `call_tool` with the returned toolset name in
`toolset_name`, the member name in `tool_name`, and an `arguments` object matching
the tool's schema. Omit `toolset_name` for a top-level tool. Never dispatch
`call_tool` through itself. Serialize calls and check each response.

When multiple editors are open, confirm which project and engine this session
reaches before changing editor state. See [instance identification](references/operations.md#identify-the-editor).

## Load relevant Unreal Agent Skills

For unfamiliar project work, discover `AgentSkillToolset`, call `ListSkills`,
and load relevant entries with `GetSkills`. These engine/project instruction
bundles are separate from this desktop plugin's three client skills. Follow
applicable project knowledge within the user's instructions and task scope.

## Compilation and editor changes

- Do not initiate Build, compilation, or Live Coding without explicit user
  authorization for that operation. A request to edit or fix code alone does not
  authorize compilation. Reuse prior authorization within its stated scope.
- Inspect tool schemas and scripts for compilation side effects before calling
  them. Tests or scripts that trigger compilation require the same authorization.
- If compilation is already running, wait or report the busy state; do not start
  another compile. Once authorized, use the actual available compile tool and
  wait for its result instead of assuming success.
- Inspect PIE state before an editor-only operation. Do not stop a running session
  without authorization when stopping it changes the user's active work.
- Preserve a recovery point before risky bulk changes. Respect requests to keep
  changes unsaved. Do not delete, move, or overwrite unrelated assets.
- Read returned status fields as well as transport errors. A successful HTTP
  response alone does not prove an asset operation or compilation succeeded.

## Connection failures and verification

Use [setup.md](references/setup.md) for setup and
[operations.md](references/operations.md) for errors, ports, stale schemas, or
optional proxy recovery. Missing tools alone do not prove the editor is stopped.

Confirm live connectivity with a successful read-only Unreal tool call, such as
reading selected actors. An empty selection is a valid result. HTTP reachability,
a proxy status, and a cached tool list are weaker checks; report them separately.
If a call fails, give the exact error and distinguish facts from hypotheses.

## Companion skills

- `create-toolset`: add or extend C++/Python ToolsetRegistry tools.
- `unreal-skill`: create or update a project/plugin Unreal Agent Skill.

Report changed objects and assets, actual validation performed, and remaining
limitations. Static inspection is not a successful UE build or runtime test.
