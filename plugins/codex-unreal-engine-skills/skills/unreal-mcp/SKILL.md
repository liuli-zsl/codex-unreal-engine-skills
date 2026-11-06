---
name: unreal-mcp
description: "Inspect or change a live Unreal Editor through Epic's official MCP. Use for actual editor or asset tasks and connection diagnosis; skip conceptual Unreal questions that need no project access."
---

# Unreal MCP for Codex

Use Epic's official Unreal MCP server and discover its live schemas. This package
changes the client integration, not the Unreal tool implementations.

## Configure the connection from the plugin page

The plugin's native settings form uses the `openai/settings` MCP extension.
Direct users to the plugin page > Manage > `unreal-mcp-settings`
(Unreal MCP 地址设置), then the **Unreal MCP 地址** field. Press Enter or leave
the field to save. Do not replace this UI with a suggested chat prompt.

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

1. Call `list_toolsets`, or go directly to `describe_toolset` when the relevant
   toolset is already clear. Read its current input and output schemas.
2. Call the advertised dispatcher `call_tool` with `toolset_name`, `tool_name`,
   and an `arguments` object matching that schema. Domain tools are not necessarily
   exposed as separate native MCP tools.
3. Omit `toolset_name` only for a tool registered directly on the MCP server.
   Never recursively dispatch `call_tool` through itself.
4. Serialize live Unreal calls. Check each response before issuing the next call,
   particularly for mutations and operations that share editor state.

Tool-search mode normally exposes only `list_toolsets`, `describe_toolset`, and
`call_tool`; three meta-tools do not mean Unreal has only three operations.

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
