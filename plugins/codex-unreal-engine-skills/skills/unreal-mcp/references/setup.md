# Codex Setup for Unreal MCP

Use this reference only when setup or connection recovery is part of the task.
Inspect the current working configuration before changing anything. Keep an
already functioning connection and user-specified endpoint.

## 1. Confirm the target project and executor

Identify the intended `.uproject` and use This computer / Local. For launcher
projects the root contains the `.uproject`; source engine workspaces may have
`GenerateProjectFiles.bat`, `.sh`, or `.command`. A bare `Engine` folder alone is
not a reliable root marker. Do not edit an unrelated project.

## 2. Enable the server and tools

In UE 5.8, enable `Unreal MCP` (`ModelContextProtocol`) and `All Toolsets`
(`AllToolsets`) through Edit > Plugins. Individual toolset plugins may replace
the aggregate when a narrower surface is wanted. The registry dependency is
enabled automatically. Restart only as part of an authorized setup action.

Inspect and preserve existing `.uproject` entries if editing the file directly.
Enabling only the transport does not guarantee the required toolsets are loaded.

## 3. Start the intended endpoint

Read the intended editor's existing settings and startup logs first. Preserve
its port and URL path. For a new setup only, UE's official defaults are:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
ServerUrlPath=/mcp
```

Per-user settings normally live in
`<Project>/Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini`.
Prefer the editor UI while it is running; do not overwrite its active settings.

When manual startup is actually needed, use the UE console and substitute the
intended editor's actual configured port for `<port>`; do not enter the angle
brackets literally:

```text
ModelContextProtocol.StartServer <port>
```

A no-argument start command may use the API default instead of a custom editor
port. Starting again can stop an existing MCP instance first. Use an explicit
port derived from the current configuration, and do not restart a working server
merely to follow this setup guide. Check the installed engine version's behavior
when diagnosing a discrepancy.

## 4. Connect the desktop client

The portable plugin's root `mcp.json` declares a Streamable HTTP connection using
UE's official first-setup default `http://127.0.0.1:8000/mcp`. This is a configurable
example, not an automatic discovery result. Prefer an already configured working
Unreal connection. For a personal endpoint, open the plugin page, try it in chat
and send its first
suggestion, **配置 Unreal MCP 地址**. Enter the URL for the editor you intend
to use. The [endpoint helper](../scripts/configure_endpoint.py) uses Python 3
and the desktop Codex CLI to save just `mcp_servers.unreal-mcp.url` in the
user's Codex settings. This applies across local projects unless a higher-priority
setting overrides it, and remains in MCP settings after the plugin is removed.
The bundled URL stays available as the installation default.
The helper backs up an existing settings file on change, preserves other fields,
and rejects a transport or authentication conflict. After saving, reconnect or
open a new local chat. The editor's listening port is configured separately.
Do not silently disable or duplicate a working user-level connection. If another
connection also targets the editor, use one explicitly; removing a duplicate is
a user-directed action.

If the host requires direct configuration, its Settings > MCP servers > Add
server supports Streamable HTTP with the same URL. The local UE server has no
token authentication by default. Keep it on loopback.

Codex local clients use `config.toml`; Claude `.mcp.json` instructions are not a
replacement. `ModelContextProtocol.GenerateClientConfig Codex` is optional and
is not needed when the plugin or existing client configuration already works.
The engine writer can refuse to overwrite an existing TOML file. Inspect and
merge only requested entries; never delete unrelated configuration to force it.

## 5. Verify the actual state

1. Check UE's `LogModelContextProtocol` and `LogHttpListener` output for startup
   and successful binding on the intended port.
2. Reconnect the desktop client when a changed connection requires it.
3. Discover the MCP tools and perform a read-only Unreal domain call, such as
   `GetSelectedActors` after reading its live schema.
4. Report an empty result as no selected actors, not a connection error.

A TCP connection or HTTP response (including 404) does not establish MCP
initialization. An initialized session or cached tool list alone does not prove
that an editor domain call can currently execute.

## Optional proxy

The upstream supports a proxy when the engine ships
`Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`. This adaptation
does not install it or change the direct HTTP connection automatically. If the
user requests it, inspect that engine version's README and client-format support
first. Do not assume a legacy `--mcp-json` installer accepts portable `mcp.json`
or writes Codex TOML correctly. See [operations.md](operations.md) for recovery
semantics and the [upstream setup reference](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/blob/main/skills/unreal-mcp/references/setup.md).
