# Unreal Engine Skills for Codex

English | [简体中文](README.zh-CN.md)

Use a local Codex session to operate Unreal Editor through MCP, read the engine workflows for your project version, or author toolsets and Agent Skills. This unofficial plugin combines Epic’s Claude Code skills with desktop access to Unreal’s built-in workflows. [Epic’s GitHub project](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin)

Version **0.1.8** supports **UE 5.8 and 5.9** in the same plugin. Its three GitHub-derived skills incorporate Epic’s **3.1.2** update.

## Install from GitHub

For most users, install from `main` with the Codex CLI. The plugin’s connection settings use Python 3, available as `python`.

```sh
codex plugin marketplace add https://github.com/liuli-zsl/codex-unreal-engine-skills.git --ref main
codex plugin add codex-unreal-engine-skills@codex-unreal-engine-skills-local
```

Open the target project in Unreal Editor, enable **Unreal MCP** and the toolsets you need (or **All Toolsets**), and confirm that the MCP server is listening. In a local Codex chat, ask “Read the selected level actors using Unreal MCP.” A successful response with an empty list means no actors are selected. If you use a custom address, set it under **Settings → Unreal Editor 连接** in the plugin details.

To follow an engine-specific maintenance branch, replace `main` with `5.8` or `5.9` in the first command. To pin a published version, use its tag, for example `--ref v0.1.6`. [GitHub Releases](https://github.com/liuli-zsl/codex-unreal-engine-skills/releases)

Use the tool catalog from the connected editor. UE 5.8 exposes `describe_toolset`. UE 5.9 Preview exposes `describe_toolsets` and `describe_tools`. When several editors are open, use distinct ports and verify the target project. See the [MCP skill](plugins/codex-unreal-engine-skills/skills/unreal-mcp/SKILL.md) and [setup guide](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md).

## Skills by source and engine version

One installation of `main` covers both series. The three GitHub skills are desktop entry points adapted from Epic's MIT-licensed Claude Code plugin. The fourth entry point, [`unreal-engine-workflows`](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/SKILL.md), is maintained here. It brings workflows found in the engine into local desktop chats. Each catalog row includes the engine provider, source path and a short workflow that ships with the plugin. The table describes built-in skill coverage. A project can expose additional tools or skills.

| Origin and workflow | UE 5.8 | UE 5.9 |
| --- | --- | --- |
| Epic GitHub · `unreal-mcp` (operate the editor), `create-toolset` (author MCP tools), `unreal-skill` (author engine skills) | All three. Use class/asset formats for engine skills. | All three. Engine-side Markdown skills are also supported. |
| UE · editor foundations and Niagara | Blueprints, outdoor lighting, materials, skill authoring. Niagara fundamentals, Blueprint interaction, cleanup, custom HLSL, level placement, optimization and renderers. | Same 11 topics. |
| UE · Dataflow, Chaos Cloth and PCG assets | Dataflow graph editing and cloth conversion. PCG graph generation, instant level operations, asset lineups, Biome Core setup and diagnosis, mesh instancing, mesh partition and shape grammar. | Same 10 topics. |
| UE · additional editor and UI workflows | — | Actor placement, asset diff, source control, UMG basics, focus navigation, Editor Utility Widgets, runtime UI diagnosis, MVVM binding, Slate input, widget animation and widget documentation. |
| UE · Sequencer, audio, rendering and deformation | — | Sequencer core, bindings, camera, Control Rig, animation tools, gameplay, Director Blueprint, import/export and keyframing. Animation Mixer, MetaSound fundamentals, pages, performance, presets, recipes, trigger topology and workflow selection. Movie Render Graph and Queue, Scene Capture diagnostics, ML Deformer and Texture Graph. |
| UE · engine and platform Markdown | — | Build diagnosis, headless runs, log triage, build trimming and its six guides (measure, code, content, shaders, delivery, validate). Wasm deployment, performance and texture sets. |
| UE · PCG Markdown | — | PCG overview, debug, manual edits, performance, low-end devices, runtime setup and validation, including Landscape and MeshTerrain variants. The MeshTerrain setup entry is a placeholder in the inspected build. |
| UE 5.9 host integrations | — | Canvas extension authoring (`unrealcanvas-extension-author`) and canvas-scoped skills require the corresponding Canvas capabilities. Unreal Assistant uses the shared editor registry. [Host details](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/canvas-assistant.md) |

**Complete lists** · [21 shared built-in workflows](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/shared.csv) · [57 additional built-in workflows for 5.9](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/ue5.9.csv). UE 5.9 has 78 distinct catalog entries. A PCG asset and its native parent count once, as do the 11 Markdown files also exposed by PCG C++ classes. Canvas library entries depend on the installation and are counted separately.

In a local desktop chat, try “For UE 5.8.4, find the built-in Niagara renderer skill and read its instructions.” The plugin identifies the target editor or its `Engine/Build/Build.version` before selecting a workflow. A running editor supplies resolved instructions through `ListSkills` and `GetSkills`, including project-specific skills. With the editor closed, desktop Codex can read the packaged workflow and the matching installation's Python, Markdown or C++ text. Blueprint assets and project-generated instructions need a matching editor for their resolved text. With only a stated version, the packaged workflow is available. [Desktop lookup and examples](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/SKILL.md#desktop-lookup)

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
| Windows desktop payload | Codex CLI `0.171.0-alpha.13.2` installed and enabled 0.1.8 in an isolated profile. The installed files matched the source. |
| UE 5.8.4 | All 21 catalog source paths checked. An isolated headless editor commandlet exposed four skills with its selected toolsets. Over MCP, `describe_toolset`, `ListSkills` and `GetSkills` returned the Blueprint Basics instructions. |
| UE 5.9.0 | All 78 catalog source paths checked. The running editor returned 87 registry keys. Through `describe_tools` and `GetSkills` we read the Blueprint Basics, PCG graph-generation asset and log-triage instructions. ML Deformer and Animation Mixer were absent from this session's list. |

For detailed installation, settings and editor checks by version, see the [changelog](Docs/CHANGELOG.md).

## Project layout

| Path | Purpose |
| --- | --- |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | Local marketplace and plugin source path. |
| [`plugins/codex-unreal-engine-skills/`](plugins/codex-unreal-engine-skills/) | Installable plugin root. |
| [`plugin.json`](plugins/codex-unreal-engine-skills/plugin.json) | Plugin identity, version, and desktop metadata. |
| [`skills/`](plugins/codex-unreal-engine-skills/skills/) | Four desktop skill entries, the versioned engine catalog and MCP references. |
| [`UPSTREAM.md`](plugins/codex-unreal-engine-skills/UPSTREAM.md) | Upstream provenance and adaptation summary. |
| [`VALIDATION.json`](VALIDATION.json) / [`upstream-changes.diff`](upstream-changes.diff) | Historical validation and skill diff prepared for 0.1.1. |
| [AGENTS.md](AGENTS.md) / [Docs/CHANGELOG.md](Docs/CHANGELOG.md) | Maintenance conventions and verified change history. |

## Development and authorization

Follow [AGENTS.md](AGENTS.md) for version and documentation updates. Preserve existing connection settings and user work. Compilation, Live Coding, and scripts that trigger compilation require explicit authorization. This package includes no build/test/cook runner.

## Support

liuli-zsl maintains this Codex adaptation. Report installation and connection problems in [GitHub Issues](https://github.com/liuli-zsl/codex-unreal-engine-skills/issues).

## License

The repository and installable plugin carry the MIT license and Epic Games’ copyright notice. [Repository license](LICENSE) · [Bundled license](plugins/codex-unreal-engine-skills/LICENSE) · [Upstream attribution](plugins/codex-unreal-engine-skills/UPSTREAM.md)
