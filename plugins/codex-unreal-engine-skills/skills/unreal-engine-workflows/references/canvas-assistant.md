# Canvas and Assistant in UE 5.9

These integration notes were checked against the 5.9.0 editor and its bundled Canvas 0.24.0 distribution. First confirm the target engine. Then check which integration the current session actually exposes.

## Working in Canvas

- For a scene, actor or Unreal asset, use the editor connection selected in Canvas. Discover the editor's skill registry, then retrieve the matching project or engine instructions. A desktop Codex session connected directly to Unreal MCP can use the same registry.
- For a canvas, its nodes or its attached instructions, use the available Canvas connection. Its session may supply `unrealcanvas` directly, or the editor may advertise a Canvas bridge toolset. Inspect the live discovery results and select one route. In a desktop session with only editor MCP, report a missing Canvas capability if the bridge does not expose it.
- Canvas can list its library with `list_skills`, load one skill with `get_skill`, and determine the effective skill selection for the current request with `resolve_skills`. The library may contain local, shared and extension entries. A library entry can be present without being active on this canvas.
- To author a Canvas extension, the service package supplies `unrealcanvas-extension-author` for its local agent. In a desktop session, inspect the host's available authoring help (`get_help`, topic `extension-authoring`). Identify the requested contribution and existing extension manifest, implement it against that host's documented extension API and check the contribution in Canvas. The `unreal-integration` and `building-a-level` help topics cover asset exchange and level assembly. Use the actual advertised help schema.
- When Canvas or its project is offline, the desktop workflow above is available for planning. User library contents, active skill selection and the host's current extension API require that Canvas connection.

The Win64 distribution is under `Engine/Plugins/Developer/UnrealCanvas/UnrealCanvasBridge/Binaries/`. The local-agent instructions and extension-author skill are embedded in the service package. The client integration in this repository ships an original overview and leaves the service package in the engine installation. [Epic's Canvas guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/getting-started-with-unreal-canvas-in-unreal-engine)

## Working in Unreal Assistant

The Assistant host provides the current editor's MCP connection and gathers project, user and toolset instructions. For a domain task such as Blueprint editing or rendering, retrieve the same `AgentSkillToolset` entries as an external client connected to that project. The inspected `Engine/Plugins/Experimental/AIAssistant/` plugin supplies this host integration. Its directory contains no standalone domain skill pack. [Epic's Unreal MCP guide](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?application_version=5.9)
