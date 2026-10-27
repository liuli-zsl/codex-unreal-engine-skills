# Unreal Engine Skills for Codex

English | [简体中文](README.zh-CN.md)

An unofficial desktop adaptation of Epic Games' [Unreal Engine Skills for Claude Code](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin), for local ChatGPT/Codex sessions. It packages client-side skills and an MCP connection to a running Unreal Editor.

Plugin ID: `codex-unreal-engine-skills`. Version: **0.1.2**. Upstream snapshot: **3.1.1**, commit `a6aa73ada02a9fb1f5415bec491f9942c519b297`.

## Included skills

| Skill | Purpose |
| --- | --- |
| `unreal-mcp` | Discover and call live Unreal Editor tools. |
| `create-toolset` | Author or extend C++/Python tools registered with ToolsetRegistry. |
| `unreal-skill` | Create or maintain engine-side Agent Skills in a project or plugin. |

The adaptation adds desktop plugin and marketplace metadata, preserves the upstream authoring examples, and replaces the Bash SessionStart hook with task-scoped skill guidance. Unreal itself supplies the MCP server and editor tools.

## Local installation and connection

This directory is the local marketplace root. Keep its hidden `.agents/` directory together with `plugins/`. The marketplace is named `codex-unreal-engine-skills-local` (display name **Codex Unreal Engine Skills Local**), and its plugin is **Unreal Engine Skills for Codex**.

The bundled endpoint is `http://127.0.0.1:8000/mcp`. Check the intended editor's actual endpoint before installation and preserve any existing working configuration. The endpoint appears in both:

- [`mcp.json`](plugins/codex-unreal-engine-skills/mcp.json)
- [`unreal-mcp/agents/openai.yaml`](plugins/codex-unreal-engine-skills/skills/unreal-mcp/agents/openai.yaml)

See the [Chinese installation guide](README.zh-CN.md#本地安装方式) and bundled [setup reference](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md). Client UI and installation support depend on the host version. Source files and installed plugin caches are separate copies; editing this directory alone does not establish that the running client has loaded those changes.

## Renaming from 0.1.1

Version 0.1.2 renames the plugin ID from `unreal-engine-chatgpt-desktop` to `codex-unreal-engine-skills`, and the marketplace ID from `ue-mcp-desktop-local` to `codex-unreal-engine-skills-local`. The source root is now `codex-unreal-engine-skills/` and the installable payload is `plugins/codex-unreal-engine-skills/`.

An existing 0.1.1 installation retains its old identity and cached files. This source rename does not update that installation. Use the renamed source for a subsequent installation and verify it separately; 0.1.2 has not yet been installed or tested in the client. The MCP server key remains `unreal-mcp`, so avoid enabling both plugin copies against the same connection unintentionally.

## Verification

With the intended editor and its MCP server running, ask:

> Use unreal-mcp to read the currently selected level actors without modifying the project.

Discover live schemas with `list_toolsets` and `describe_toolset`, then use `call_tool` to dispatch the read operation. An empty selection is valid.

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
