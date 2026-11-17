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

In UE 5.8 and 5.9 Preview, check `Unreal MCP` (`ModelContextProtocol`) and `All Toolsets`
(`AllToolsets`) through Edit > Plugins. Individual toolset plugins may replace
the aggregate when a narrower surface is wanted. The registry dependency is
enabled automatically. Restart only as part of an authorized setup action.

Inspect and preserve existing `.uproject` entries if editing the file directly.
Enabling only the transport does not guarantee the required toolsets are loaded.

## 3. Start the intended endpoint

Read the intended editor's existing settings and startup logs first. Preserve
its port and URL path. UE 5.8 documents auto-start as off by default. In 5.9
Preview it defaults to on, under Editor Preferences > Agentic Workflows > Model
Context Protocol. In the example below use the section for your engine and
put the three values under that section.

| Engine | Section in `EditorPerProjectUserSettings.ini` |
| --- | --- |
| UE 5.8 | `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]` |
| UE 5.9 Preview | `[/Script/ModelContextProtocol.ModelContextProtocolSettings]` |

```ini
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
Unreal connection. Open the plugin details page > Settings > Unreal Editor 连接.
Edit **IP**, **URL 路径** (path) and **端口号** (port) separately; press Enter or
leave a field to save. Defaults are `127.0.0.1`, `/mcp`, and `8000`. IP accepts
IPv4, IPv6 or a hostname without a scheme, port or path. Port must be an integer
from 1 to 65535; path must start with `/` and contain no whitespace, query or
fragment. Invalid input is rejected. Existing HTTPS is preserved by field edits.

**恢复默认值** invokes the same-server `reset_defaults` action with no arguments
and saves the default HTTP URL. Reopen the plugin page to refresh its fields
after the action. A malformed stored URL displays defaults with a recovery note
without writing anything until the user clicks reset. Transport, authentication
and managed-configuration conflicts still require resolving the actual conflict.
The reset changes the client URL, not UE settings, and works while UE is offline.

The additional local stdio [settings server](../scripts/settings_server.py)
advertises the official [`openai/settings` extension](https://developers.openai.com/plugins/build/extensions).
The host renders the input and calls its read/update tools directly. Python 3
and a desktop host supporting structured MCP settings are required. The service
works independently of the editor's HTTP connection, including while UE is
offline. It does not proxy editor tools.

The [endpoint helper](../scripts/configure_endpoint.py) uses Codex's configuration
API to save only `mcp_servers.unreal-mcp.url` in user settings. This applies
across local projects unless a higher-priority setting overrides it, and remains
configured after removing the plugin. The bundled URL remains the installation
default. The helper backs up the existing config on change, preserves other
fields, rejects authentication/transport conflicts, and verifies the saved URL.
On Windows, it uses the launching Codex executable when MCP's filtered environment
omits the desktop CLI variable. The settings service recovers its profile from
the installed `PLUGIN_ROOT` cache layout; an unknown layout is an error, not a
reason to write another profile. Other operating systems are unverified.

After saving, reconnect MCP or open a new local chat. Restart Codex if a plugin
upgrade has not refreshed its settings service. Configure the editor's listening
port separately.
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

## Several editors on the same machine

Give each concurrently running editor a fixed port via its project preferences
or the launch argument `-ModelContextProtocolPort=<port>`. A second editor
cannot bind the same address and port. A client using the first port will keep
reaching the first editor. The plugin settings form saves one user-level URL
across projects. For simultaneous connections, configure distinct MCP server
entries in the client or use workspace-specific overrides. Switching Git
branches does not select an editor. [Verify the instance](operations.md#identify-the-editor)
through the intended connection.

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
