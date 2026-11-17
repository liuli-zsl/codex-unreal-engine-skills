# Upstream and adaptation

Original: https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin
Reviewed upstream commit: `a6aa73ada02a9fb1f5415bec491f9942c519b297` (plugin manifest version 3.1.1).
Desktop adaptation version: 0.1.1, prepared on 2026-10-14.

This is a local adaptation, not an official Epic Games or OpenAI distribution.
The upstream MIT license is preserved verbatim in LICENSE. The original C++ and
Python fenced examples in create-toolset and unreal-skill are retained.

Changes: portable Agent Plugins manifests; local marketplace descriptor;
ChatGPT/Codex desktop skill metadata; configurable official first-setup defaults;
existing-configuration precedence; explicit compilation
authorization; serialized live calls; actual read-only MCP verification;
desktop-specific setup instructions replacing Claude client setup.

The Bash SessionStart hook is replaced by task-scoped skill guidance. There is
no auto-executing lifecycle hook or bundled build/test/cook runner.

On 2026-11-17 the adaptation incorporated the multi-editor guidance from
[upstream 3.1.2](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/commit/0e27bde2b55c5d3f6948532f4296aaa3654d8f4b).
The client retains its Codex settings workflow. The version-aware discovery
instructions were checked separately against Epic's
[UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.8)
and [UE 5.9 Preview](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.9) documentation.

References:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/deploy/connect-chatgpt
- https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
