# Unreal Engine Skills for Codex

English | [简体中文](README.zh-CN.md)

An unofficial desktop adaptation of Epic Games' [Unreal Engine Skills for Claude Code](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin), for local ChatGPT/Codex sessions. It packages client-side skills and an MCP connection to a running Unreal Editor.

Plugin ID: `codex-unreal-engine-skills`. Version: **0.1.6**. Based on Epic’s **3.1.2**, commit `0e27bde2b55c5d3f6948532f4296aaa3654d8f4b`.

`main` tracks the latest adaptation for UE 5.8 and 5.9 Preview. The `5.8` and `5.9` branches track their respective engine lines.

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

Open the plugin details page and find **Settings > Unreal Editor 连接**. Edit **IP**, **URL 路径** (URL path), and **端口号** (port) separately; press Enter or leave each field to save. Defaults are `127.0.0.1`, `/mcp`, and `8000`. The IP field also accepts IPv6 and hostnames. Ports must be integers from 1 to 65535; paths must start with `/` and contain no whitespace, query, or fragment. Invalid input is rejected without changing the saved address. **恢复默认值** (Restore defaults) saves `http://127.0.0.1:8000/mcp` in one action; reopen the page to refresh the displayed fields. Ordinary field edits preserve an existing HTTPS scheme. Opening or upgrading the plugin never resets a custom address. This uses the official [`openai/settings` extension](https://developers.openai.com/plugins/build/extensions), not a chat prompt. The local settings server needs Python 3 and a desktop Codex host supporting structured MCP settings. It works while Unreal is offline, backs up the existing user config, and changes only `mcp_servers.unreal-mcp.url`. Reconnect MCP or open a new local chat after saving.

The user address applies across your local projects, survives a plugin update, and can also be managed in Codex MCP settings. The resulting user connection stays configured when the plugin is removed. The Unreal Editor must listen on the same address. The bundled first-install default is `http://127.0.0.1:8000/mcp`.

See the [Chinese installation guide](README.zh-CN.md#本地安装方式) and bundled [setup reference](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md). Client UI and installation support depend on the host version. Source files and installed plugin caches are separate copies; editing this directory alone does not establish that the running client has loaded those changes.

## Renaming from 0.1.1

Version 0.1.2 renames the plugin ID from `unreal-engine-chatgpt-desktop` to `codex-unreal-engine-skills`, and the marketplace ID from `ue-mcp-desktop-local` to `codex-unreal-engine-skills-local`. The source root is now `codex-unreal-engine-skills/` and the installable payload is `plugins/codex-unreal-engine-skills/`.

An existing 0.1.1 installation retains its old identity and cached files. This source rename does not update that installation. Use the renamed source for a subsequent installation and verify it separately. The MCP server key remains `unreal-mcp`, so avoid enabling both plugin copies against the same connection unintentionally.

## Verification

With the intended editor and its MCP server running, ask:

> Use unreal-mcp to read the currently selected level actors without modifying the project.

Inspect the advertised schema, dispatch the read and check the result. An empty selection is valid.

For 0.1.6, discovery names, parameters and configuration sections were checked against UE 5.8.4 and 5.9 Preview source and configuration. Package manifests, links and skill entries passed static checks. Installation and a live editor call remain unverified for this version.

Version 0.1.5 was installed in an isolated Windows desktop CLI profile (Codex 0.166.0-alpha.6, Python 3.11). The actual host discovered `openai/settings` and successfully called read, partial update and reset tools. Independent field edits, reset persistence, 21 invalid inputs, port boundaries, IPv6, existing HTTPS/hostname URLs, damaged-URL recovery, backups, unchanged sibling settings, authentication protection and disabled-state preservation passed. Desktop clicks/rendering and a live editor call were not part of this check; other operating systems are unverified. The settings process resolves its installed Codex profile from `PLUGIN_ROOT` and uses the launching desktop CLI on Windows, avoiding an unrelated older CLI on PATH.

On **2026-10-27**, the existing 0.1.1 installation exposed all three skills and the MCP tools. At that time, its plugin files matched the 0.1.1 source copy before documentation changes. `list_toolsets`, `describe_toolset`, and `GetSelectedActors` succeeded; the latter returned one selected actor. This verifies the existing installation's read-only connection, not a clean installation, asset editing, compilation, or every toolset. See [CHANGELOG.md](CHANGELOG.md).

[`VALIDATION.json`](VALIDATION.json) records checks from package preparation; it is a historical snapshot, not the current acceptance report.

## Project layout

| Path | Purpose |
| --- | --- |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | Local marketplace and plugin source path. |
| [`plugins/codex-unreal-engine-skills/`](plugins/codex-unreal-engine-skills/) | Installable plugin root. |
| [`plugin.json`](plugins/codex-unreal-engine-skills/plugin.json) | Plugin identity, version, and desktop metadata. |
| [`skills/`](plugins/codex-unreal-engine-skills/skills/) | Three skills, metadata, and MCP references. |
| [`UPSTREAM.md`](plugins/codex-unreal-engine-skills/UPSTREAM.md) | Upstream provenance and adaptation summary. |
| [`upstream-changes.diff`](upstream-changes.diff) | Historical skill diff prepared for 0.1.1. |
| [AGENTS.md](AGENTS.md) / [CHANGELOG.md](CHANGELOG.md) | Maintenance conventions and verified change history. |

## Development and authorization

Follow [AGENTS.md](AGENTS.md) for version and documentation updates. Preserve existing connection settings and user work. Compilation, Live Coding, and scripts that trigger compilation require explicit authorization. This package includes no build/test/cook runner.

## License

[MIT](plugins/codex-unreal-engine-skills/LICENSE), retaining Epic Games' copyright notice. This adaptation is not an official Epic Games or OpenAI distribution. See [UPSTREAM.md](plugins/codex-unreal-engine-skills/UPSTREAM.md).
