# Unreal Engine Skills for Codex

English | [简体中文](README.zh-CN.md)

Use a local Codex session to inspect and edit a running Unreal Editor through MCP, or to author toolsets and Unreal Agent Skills. This is an unofficial adaptation of Epic Games' [Unreal Engine Skills for Claude Code](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin).

This checkout contains **0.1.7** of `codex-unreal-engine-skills`, based on Epic’s **3.1.2** at commit `0e27bde2b55c5d3f6948532f4296aaa3654d8f4b`.

## Install from GitHub

For most users, install from `main` with the Codex CLI. The plugin’s connection settings use Python 3, available as `python`.

```sh
codex plugin marketplace add https://github.com/liuli-zsl/codex-unreal-engine-skills.git --ref main
codex plugin add codex-unreal-engine-skills@codex-unreal-engine-skills-local
```

Open the target project in Unreal Editor, enable **Unreal MCP** and the toolsets you need (or **All Toolsets**), and confirm that the MCP server is listening. In a local Codex chat, ask “Read the selected level actors using Unreal MCP.” A successful response with an empty list means no actors are selected. If you use a custom address, set it under **Settings → Unreal Editor 连接** in the plugin details.

To follow an engine-specific maintenance branch, replace `main` with `5.8` or `5.9` in the first command. To pin a published version, use its tag, for example `--ref v0.1.6`. [GitHub Releases](https://github.com/liuli-zsl/codex-unreal-engine-skills/releases)

Use the tool catalog from the connected editor. UE 5.8 exposes `describe_toolset`. UE 5.9 Preview exposes `describe_toolsets` and `describe_tools`. When several editors are open, use distinct ports and verify the target project. See the [MCP skill](plugins/codex-unreal-engine-skills/skills/unreal-mcp/SKILL.md) and [setup guide](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md).

## Included skills

| Skill | Purpose |
| --- | --- |
| `unreal-mcp` | Discover and call live Unreal Editor tools. |
| `create-toolset` | Author or extend C++/Python tools registered with ToolsetRegistry. |
| `unreal-skill` | Create or maintain engine-side Agent Skills in a project or plugin. |

The adaptation adds desktop plugin and marketplace metadata, preserves the upstream authoring examples, and replaces the Bash SessionStart hook with task-scoped skill guidance. Unreal itself supplies the MCP server and editor tools.

## Local installation and connection

This directory is the local marketplace root. Keep its hidden `.agents/` directory together with `plugins/`. The marketplace is named `codex-unreal-engine-skills-local` (display name **Codex Unreal Engine Skills Local**), and its plugin is **Unreal Engine Skills for Codex**.

For a fresh installation from this checkout, run `codex plugin marketplace add .` in the repository root, then run the same `codex plugin add` command shown above.

Open the plugin details page and find **Settings > Unreal Editor 连接**. Edit **IP**, **URL 路径** (URL path), and **端口号** (port) separately; press Enter or leave each field to save. Defaults are `127.0.0.1`, `/mcp`, and `8000`. The IP field also accepts IPv6 and hostnames. Ports must be integers from 1 to 65535; paths must start with `/` and contain no whitespace, query, or fragment. Invalid input is rejected without changing the saved address. **恢复默认值** (Restore defaults) saves `http://127.0.0.1:8000/mcp` in one action; reopen the page to refresh the displayed fields. Ordinary field edits preserve an existing HTTPS scheme. Opening or upgrading the plugin never resets a custom address. This uses the official [`openai/settings` extension](https://developers.openai.com/plugins/build/extensions), not a chat prompt. The local settings server needs Python 3 and a desktop Codex host supporting structured MCP settings. It works while Unreal is offline, backs up the existing user config, and changes only `mcp_servers.unreal-mcp.url`. Reconnect MCP or open a new local chat after saving.

The user address applies across your local projects, survives a plugin update, and can also be managed in Codex MCP settings. The resulting user connection stays configured when the plugin is removed. The Unreal Editor must listen on the same address. The bundled first-install default is `http://127.0.0.1:8000/mcp`.

See the [Chinese installation guide](README.zh-CN.md#本地安装方式) and bundled [setup reference](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md). Client UI and installation support depend on the host version. Source files and installed plugin caches are separate copies; editing this directory alone does not establish that the running client has loaded those changes.

## Renaming from 0.1.1

Version 0.1.2 renames the plugin ID from `unreal-engine-chatgpt-desktop` to `codex-unreal-engine-skills`, and the marketplace ID from `ue-mcp-desktop-local` to `codex-unreal-engine-skills-local`. The source root is now `codex-unreal-engine-skills/` and the installable payload is `plugins/codex-unreal-engine-skills/`.

An existing 0.1.1 installation retains its old identity and cached files. This source rename does not update that installation. Use the renamed source for a subsequent installation and verify it separately. The MCP server key remains `unreal-mcp`, so avoid enabling both plugin copies against the same connection unintentionally.

## Verification

| Scope | Result |
| --- | --- |
| Windows installation from this checkout, 2026-11-26 | Codex CLI `0.171.0-alpha.13.2` installed and enabled 0.1.7 in a fresh profile. All 15 installed files matched the source. |
| UE 5.9 Preview | On 2026-11-17, plugin 0.1.6 queried the live schema with `describe_tools` and called `GetSelectedActors` through `call_tool`. The editor returned an empty selection. |
| UE 5.8.4 | Tool names, parameters and settings were checked against engine source and configuration for plugin 0.1.6. A live editor read is still pending. |

For detailed installation, settings and editor checks by version, see the [changelog](Docs/CHANGELOG.md).

## Project layout

| Path | Purpose |
| --- | --- |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | Local marketplace and plugin source path. |
| [`plugins/codex-unreal-engine-skills/`](plugins/codex-unreal-engine-skills/) | Installable plugin root. |
| [`plugin.json`](plugins/codex-unreal-engine-skills/plugin.json) | Plugin identity, version, and desktop metadata. |
| [`skills/`](plugins/codex-unreal-engine-skills/skills/) | Three skills, metadata, and MCP references. |
| [`UPSTREAM.md`](plugins/codex-unreal-engine-skills/UPSTREAM.md) | Upstream provenance and adaptation summary. |
| [`VALIDATION.json`](VALIDATION.json) / [`upstream-changes.diff`](upstream-changes.diff) | Historical validation and skill diff prepared for 0.1.1. |
| [AGENTS.md](AGENTS.md) / [Docs/CHANGELOG.md](Docs/CHANGELOG.md) | Maintenance conventions and verified change history. |

## Development and authorization

Follow [AGENTS.md](AGENTS.md) for version and documentation updates. Preserve existing connection settings and user work. Compilation, Live Coding, and scripts that trigger compilation require explicit authorization. This package includes no build/test/cook runner.

## Support

liuli-zsl maintains this Codex adaptation. Report installation and connection problems in [GitHub Issues](https://github.com/liuli-zsl/codex-unreal-engine-skills/issues).

## License

The repository and installable plugin carry the MIT license and Epic Games’ copyright notice. [Repository license](LICENSE) · [Bundled license](plugins/codex-unreal-engine-skills/LICENSE) · [Upstream attribution](plugins/codex-unreal-engine-skills/UPSTREAM.md)
