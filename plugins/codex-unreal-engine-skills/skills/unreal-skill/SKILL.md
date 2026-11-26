---
name: unreal-skill
description: "Create, edit, or review Unreal Agent Skills registered in a project or plugin. These are engine-side instruction bundles, not ChatGPT client skills or MCP tool implementations."
---

# Unreal Skill

## Desktop adaptation and authorization

Explicit user instructions take precedence over this skill. Use the already
configured Unreal MCP connection for live queries and inspect its actual schema.
Resolve its endpoint from existing configuration; do not assume the bundled
first-setup default matches a running editor. Serialize live calls.

Do not execute Build, compilation, Live Coding, or a test/script that triggers
compilation without explicit user authorization covering that operation. An edit
request alone does not grant it. Reuse authorization already given within scope.
Compilation/testing guidance below applies after the relevant authorization.

Preserve existing user work. A scoped request to create or edit a tool or skill
authorizes that requested work; do not add repeated confirmation steps for it.
Ask only when a missing decision materially changes scope or risk. Distinguish
source inspection, compilation, and actual editor/runtime verification.

You are authoring an Unreal Engine Agent Skill: a named, reusable bundle of instructions that packages essential knowledge the agent either doesn't know or needs to pay close attention to. A skill can provide general best practices in a domain, guidance on a specific workflow, or a mix of both.

## Principles

A good skill is:

**Novel**: The content should be things the agent doesn't already know or can't learn by using tools. If the agent could figure it out by calling a tool, don't put it in a skill.

**Collegial**: Write like you're briefing a knowledgeable colleague, not authoring documentation. Assume the reader understands Unreal. Give them what they need to act, not a full explanation of how everything works.

**Flexible**: Skills can include conceptual explanations, step-by-step instructions, or a mix. Use whichever form makes the guidance clearest for the task.

**Durable**: Don't embed property names, tool names, or other details that change over time. Skills that reference specific API names break silently when those names change.

**Agnostic**: Don't reference orchestration systems, role names, model names, or anything about how the agent is wired up. Skills should work regardless of the surrounding infrastructure.

**Parsimonious**: Every token costs context. Put them where they matter most and cut anything that isn't essential or evergreen. If a sentence wouldn't be missed, remove it.

## Before You Write

Work through these questions before writing anything.

**1. Does the skill already exist?** Check the [built-in catalog for the target engine](../unreal-engine-workflows/SKILL.md). In the connected project use `ListSkills` and `GetSkills` to include project-specific entries and read the resolved instructions before deciding whether a new skill is needed.

**2. Choose the implementation path.** Check which formats the target engine loads.

- **Markdown (UE 5.9 Preview)**. Place `SKILL.md` in `<Project>/Skills/<folder>/` or `<EnabledPlugin>/Skills/<folder>/`. Supply `name` and `description` in YAML frontmatter followed by the instructions. Verify its returned skill key with `ListSkills` and `GetSkills`.

- **Python class**: The right choice when the skill is part of a code plugin. It lives alongside the plugin's Python toolsets, is version-controlled with the plugin, and is registered automatically when the plugin loads.
- **UAsset**: The right choice when the skill is project-specific and doesn't belong in a plugin. Create it directly in the Content Browser using `CreateSkill` via MCP. No code required.

## Structure

Every Unreal skill has two fields.

**Description**: Loaded at discovery time, before the skill's full instructions are read. One or two sentences that clearly describe what the skill covers and when it applies.

**Instructions**: The skill's payload. The actual guidance the agent follows when the skill is active. Apply the principles above: focus on what tools can't teach and cut anything not essential.

Write instructions against the [connected editor's discovery workflow](../unreal-mcp/SKILL.md#discover-then-dispatch). Use the tool names and schemas that editor advertises.

## Python Skills

A Python skill is a `UAgentSkill` subclass defined in a Python file inside a plugin. Use this path when the skill belongs to a code plugin and should be version-controlled with the plugin.

### Authoring

Decorate the class with `@agent_skill` and inherit from `unreal.AgentSkill`. The two fields from the Structure section map to class attributes:

- The class docstring becomes the `Description`. Keep it to one or two sentences.
- `instructions` is a class attribute string containing the guidance loaded when the skill activates.

```python
import unreal

from toolset_registry.agent_skill import agent_skill

_INSTRUCTIONS = (
    'Do X before Y, because Z.\n'
    'Always verify the result after performing the operation.\n'
)

@agent_skill
class MySkill(unreal.AgentSkill):
    """Provides guidance on doing X in Unreal Engine.
    Apply this skill whenever the user wants to accomplish X."""

    instructions = _INSTRUCTIONS
```

### Registration

Skills register themselves on import. Unless directed otherwise, place skill files in a `skills/` subfolder within the plugin's Python package, import each one explicitly in that subfolder's `__init__.py`, and ensure `init_unreal.py` imports the `skills` package.

### Reloading

After editing a Python skill, reload the plugin's package before verifying. The editor won't pick up changes otherwise. Enable Remote Execution in **Edit → Project Settings → Plugins → Python → Enable Remote Execution**, then run:

```bash
python Engine/Plugins/Experimental/ToolsetRegistry/Content/Python/toolset_registry/tests/reload_remote.py your_plugin
```

## UAsset Skills

A UAsset skill is a `UAgentSkill` instance saved as a Content Browser asset. Use this path for project-specific skills that don't belong in a plugin and require no code.

### Authoring

Use `AgentSkillToolset` via MCP. Start by calling `ListSkills` to see what exists, then either create or update:

**Creating**: Call `CreateSkill` with:
- `FolderPath`: Content Browser folder, e.g. `/Game/Skills/`
- `AssetName`: PascalCase name, e.g. `MyWorkflowSkill`
- `Description`: one or two sentences (see Structure above)
- `Details`: a `FAgentSkillDetails` with `Instructions`

**Updating**: Call `UpdateSkill` with:
- `SkillPath`: full path to the skill, e.g. `/Game/Skills/MyWorkflowSkill.MyWorkflowSkill_C`
- `Description`: revised description
- `Details`: revised `FAgentSkillDetails`

## Reviewing Your Work

Before handing off, verify the skill looks right by calling `GetSkills` on its path. Then read the description and instructions together as the agent will see them:

- **Description**: Does it clearly say when this skill applies? Would an agent reading only the description know whether to activate it for a given task?
- **Instructions**: Do they teach something the agent couldn't learn from the tools? Are they brief enough to be worth the context cost?
