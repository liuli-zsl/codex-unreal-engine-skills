---
name: unreal-engine-workflows
description: "Find and read built-in Unreal Engine 5.8 or 5.9 workflows from desktop Codex for editor, asset, VFX, PCG, animation, audio or build tasks. Use for choosing an existing engine skill and for Canvas skill lookup."
---

# Use a built-in Unreal workflow

1. Identify the target engine and project. In a connected editor use its reported version or read `Engine/Build/Build.version` from the engine directory for that instance. Offline, use the user's stated target or that installation's build file. A marketplace branch, port, tool name or another installed engine cannot establish the version. Recheck after switching editors. When the version is unknown, discovery can proceed, but defer version-specific guidance. If the user explicitly asks for a comparison, label each series separately.
2. Match the task to the [shared catalog](references/shared.csv) for 5.8 and 5.9. On 5.9 also use the [5.9 additions](references/ue5.9.csv). Every row has a searchable ID, the engine provider, a path relative to `Engine/` and an independently written workflow. Those IDs identify built-in topics. Projects and plugins can supply additional or customized skills.
3. **With an editor**, follow [Unreal MCP discovery](../unreal-mcp/SKILL.md#discover-then-dispatch). Call the advertised `AgentSkillToolset.ListSkills`, match the topic to the returned descriptions and pass only returned keys to `GetSkills` using its live schema. Read the full instructions for the task, including applicable project-specific guidance. A missing entry may mean its plugin is disabled or it was filtered. Use the desktop guidance for planning and report the missing capability before any dependent editor action. Run live calls serially.
4. **Outside the editor**, the version-filtered reader below returns the packaged guidance. With the target engine installed it can also read its full static Python, Markdown or C++ definition. A Blueprint asset or a prompt that incorporates the current project gets its complete resolved text from `GetSkills`. Source instructions and offline plans do not establish that an editor operation ran. Respect scope for editing, saving, compilation, Live Coding and any script that may trigger a build.

## Desktop lookup

Run from this skill directory, or invoke [the reader](scripts/engine_workflows.py) by its installed path. `--engine` accepts the installation root or its `Engine` subdirectory. A version-only lookup works without an editor or engine installation.

```sh
python scripts/engine_workflows.py --version 5.8
python scripts/engine_workflows.py --version 5.9 --show SequencerCameraSkill
python scripts/engine_workflows.py --engine "<target engine root>" --show BlueprintBasicsSkill --source
```

With both `--engine` and `--version`, the reader checks that they agree. `--show` accepts an exact catalog ID. `--source` prints local text and its path for following relative references. Compiling code, running an engine script and loading editor assets are separate operations.

## Unreal Canvas and Unreal Assistant

On UE 5.9, use the [Canvas and Assistant reference](references/canvas-assistant.md) when the user asks about a Canvas extension, a skill attached to a canvas, or how Assistant reaches engine skills. Match the actual host and discover the available tools on that connection.
