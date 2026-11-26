# Unreal Engine Skills for Codex

[English](README.md) | 简体中文

在 ChatGPT 桌面版的 Codex 本机会话中，通过 MCP 操作 Unreal Editor、读取目标版本的引擎技能，或开发工具集和 Agent Skill。本插件将 Epic 的 Claude Code 技能与引擎自带工作流接入桌面，为非官方适配版。

当前版本 **0.1.8**，同一插件支持 **UE 5.8 和 5.9**。逐版改动和验证记录见[变更记录](Docs/CHANGELOG.md)。

## 从 GitHub 安装

日常使用选 `main`。安装需要 Codex CLI，插件的连接设置需要能通过 `python` 启动的 Python 3。

```sh
codex plugin marketplace add https://github.com/liuli-zsl/codex-unreal-engine-skills.git --ref main
codex plugin add codex-unreal-engine-skills@codex-unreal-engine-skills-local
```

用 Unreal Editor 打开目标工程，启用 **Unreal MCP** 和需要的工具集（也可启用 **All Toolsets**），确认 MCP 服务已监听。在 Codex 本地聊天中输入“通过 Unreal MCP 读取当前选中的关卡 Actor”。调用成功且返回空列表，表示当前没有选中 Actor。使用自定义地址时，在插件详情页的 **设置 → Unreal Editor 连接** 中填写。

需要跟踪某个引擎系列时，把第一行的 `main` 换成 `5.8` 或 `5.9`。要固定安装已发布的版本，使用对应标签，例如 `--ref v0.1.6`。[GitHub 发布记录](https://github.com/liuli-zsl/codex-unreal-engine-skills/releases)

UE 5.8 用 `describe_toolset` 查询工具参数，5.9 Preview 用 `describe_toolsets` 或 `describe_tools`。插件按当前编辑器实际提供的工具选择流程。多个编辑器并行时，为各实例分配独立端口，并核对当前连接的工程。[工具调用流程](plugins/codex-unreal-engine-skills/skills/unreal-mcp/SKILL.md) · [连接配置](plugins/codex-unreal-engine-skills/skills/unreal-mcp/references/setup.md)

## 技能来源与 UE 版本

同一份 `main` 插件同时支持 UE 5.8 和 5.9。前三个桌面技能适配自 Epic 为 Claude Code 发布的 MIT 开源插件。第四个入口 [`unreal-engine-workflows`](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/SKILL.md) 由本项目编写，将引擎自带的工作流接入桌面聊天。清单中每项都标有提供它的引擎模块、源码位置和随包可读的操作指引。表格按引擎安装中自带的技能统计，项目还可以提供其他工具或技能。

| 来源与工作流 | UE 5.8 可用 | UE 5.9 可用 |
| --- | --- | --- |
| Epic 官方 GitHub · `unreal-mcp` 操作编辑器，`create-toolset` 编写 MCP 工具，`unreal-skill` 编写引擎技能 | 三项均可用。引擎技能采用类或蓝图资产。 | 三项均可用。引擎也支持 Markdown 技能。 |
| UE 自带 · 编辑器基础与 Niagara | 蓝图、室外光照、材质、技能编写。Niagara 基础、蓝图交互、清理、自定义 HLSL、关卡放置、优化、渲染器。 | 同左，共 11 项。 |
| UE 自带 · Dataflow、Chaos Cloth、PCG 资产 | Dataflow 图编辑、布料转换。PCG 图生成、关卡批处理、资产陈列、Biome Core 配置与排错、网格实例化、网格分区、形状语法。 | 同左，共 10 项。 |
| UE 自带 · 新增编辑器和 UI 工作流 | — | Actor 放置、资产差异比较、版本控制、UMG 基础、焦点导航、编辑器实用控件、运行时 UI 排错、MVVM 绑定、Slate 输入、控件动画、控件说明文档。 |
| UE 自带 · Sequencer、音频、渲染与变形 | — | Sequencer 核心、绑定、相机、Control Rig、动画工具、玩法事件、Director 蓝图、导入导出、关键帧，以及动画混合器。MetaSound 基础、分页、性能、预设、配方、触发拓扑、工作流选择。另含电影渲染图与队列、Scene Capture 诊断、ML Deformer、Texture Graph。 |
| UE 自带 · 引擎与平台 Markdown | — | 构建诊断、无界面运行、日志分析、体积裁剪及 6 个专题（测量、代码、内容、着色器、交付、验证）。另有 Wasm 部署、性能、纹理集。 |
| UE 自带 · PCG Markdown | — | PCG 总览、调试、手动编辑、性能、低端设备、运行时生成配置与验证，包括 Landscape 和 MeshTerrain 两套分支。当前引擎的 MeshTerrain 配置条目是占位说明。 |
| UE 5.9 宿主集成 | — | Canvas 扩展编写（`unrealcanvas-extension-author`）和画布技能按当前 Canvas 实际能力使用。Unreal Assistant 沿用编辑器技能注册表。[宿主说明](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/canvas-assistant.md) |

**完整逐项清单** · [5.8 和 5.9 共用的 21 项](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/shared.csv) · [5.9 新增的 57 项](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/references/ue5.9.csv)。5.9 合计 78 项。PCG 图生成的蓝图资产和原生父类合计一项，11 个 PCG C++ 类与它们读取的 Markdown 也各算一次。Canvas 技能库随安装和扩展变化，单独列出。

在桌面本机会话里可以问“我的目标是 UE 5.8.4，请找到 Niagara 渲染器技能并读取指引”。插件先核对目标编辑器或其 `Engine/Build/Build.version`。编辑器在线时，通过 `ListSkills` 和 `GetSkills` 读取当前项目实际提供的完整正文。编辑器关闭时，仍可查阅随包指引，以及对应引擎安装中的 Python、Markdown 和 C++ 文本。蓝图资产与依赖项目动态生成的指引需要对应编辑器解析。仅指定版本也能读随包指引。[桌面查询方法与示例](plugins/codex-unreal-engine-skills/skills/unreal-engine-workflows/SKILL.md#desktop-lookup)

## 先看验证范围

| 范围 | 结果 |
| --- | --- |
| Windows 桌面安装包 | Codex CLI `0.171.0-alpha.13.2` 已在独立配置中安装并启用 0.1.8，安装文件与源码一致。 |
| UE 5.8.4 | 已逐项核对 21 个源码位置。在临时空工程启动无界面 Commandlet，所选工具集提供 4 项技能。通过 MCP 的 `describe_toolset`、`ListSkills` 和 `GetSkills` 成功读取蓝图基础正文。 |
| UE 5.9.0 | 已逐项核对 78 个源码位置。运行中的编辑器返回 87 个注册键，通过 `describe_tools` 和 `GetSkills` 实际读取蓝图基础、PCG 图生成蓝图资产及日志分析正文。该会话未列出 ML Deformer 和动画混合器。 |

各版本的安装、连接设置和编辑器调用详情见[变更记录](Docs/CHANGELOG.md)。

## 从旧名称迁移

0.1.2 将插件标识从 `unreal-engine-chatgpt-desktop` 改为 `codex-unreal-engine-skills`，
显示名称改为 `Unreal Engine Skills for Codex`；本地 marketplace 标识从
`ue-mcp-desktop-local` 改为 `codex-unreal-engine-skills-local`。
源码根目录和可安装插件子目录均使用新名称。

现有 0.1.1 安装仍保留原标识与缓存，源码改名不会自动更新它。
升级时从新目录安装并单独验证连接。
MCP 服务键仍为 `unreal-mcp`，安装时注意避免无意同时启用两份插件连接。

## 本地安装方式

从本地源码首次安装时，可在仓库根目录运行 `codex plugin marketplace add .`，再运行上方的 `codex plugin add` 命令。使用桌面界面安装时按以下步骤操作。

1. 获取完整的 `codex-unreal-engine-skills` 源码目录，保留 `.agents` 目录。
2. 在 ChatGPT 桌面端的 Codex/本机模式中，将
   `codex-unreal-engine-skills` 文件夹添加为一个项目并打开。
   这个文件夹是本地插件目录的根，包含 `.agents/plugins/marketplace.json`。
3. 在目标 UE 编辑器中确认 MCP 监听端口和路径，记下完整地址。
4. 重启桌面端。打开 Plugins Directory / 插件目录，选择本地来源
   `Codex Unreal Engine Skills Local`，安装 `Unreal Engine Skills for Codex`。
   实际入口名称可能随客户端语言、版本和工作区策略变化。
5. 安装后回到 UE 工程项目，新建 This computer / Local 会话，启用本插件。
6. 用 UE 打开工程并保持 MCP 运行，再发送下面的只读请求：

```text
使用 unreal-mcp 技能，通过实际 MCP 工具读取当前选中的关卡 Actor。
只返回名称和类型，不修改工程；没有选中对象就明确说明。
```

本地来源未出现时，先对照官方的本地 marketplace 说明核对目录根和客户端支持，
不要把本机 HTTP 地址改成公网地址来尝试解决。
官方说明：https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually

当前目录提供本地 marketplace 源文件，不包含安装 ZIP 附件。

## 现有连接和端口

先读取已存在且可用的 `unreal-mcp` 连接，再核对目标 UE 编辑器的 MCP 启动日志、
端口和 URL 路径。使用自定义端口、多个编辑器或代理时，不应假设默认示例适用。
已有可用连接优先。下面的配置流程会在你提交地址后保存个人设置。

打开插件详情页，找到 **设置 → Unreal Editor 连接**，直接在原生表单中修改，无需进入聊天。页面通过官方 [`openai/settings` 扩展](https://developers.openai.com/plugins/build/extensions) 提供三个输入项。

| 输入项 | 默认值 | 校验 |
| --- | --- | --- |
| IP | `127.0.0.1` | 支持 IPv4、IPv6 或主机名，不要填写协议、端口或路径。 |
| URL 路径 | `/mcp` | 以 `/` 开头，不包含空格、查询参数或片段。 |
| 端口号 | `8000` | 1–65535 的整数。 |

1. 每项按 Enter 或移开焦点保存；只修改这一项，非法输入不会写入。**恢复默认值** 按钮会一次保存 `http://127.0.0.1:8000/mcp`；点击后重新打开页面刷新显示。普通字段编辑保留原有 HTTPS 协议；升级或打开页面不会覆盖自定义地址。
2. 本地设置服务需要 Python 3 和支持原生 MCP 设置的桌面版 Codex；UE 未启动时也能配置。只更新个人设置 `mcp_servers.unreal-mcp.url`，写入前备份，保存后回读。已有认证或其他传输方式的同名连接会拒绝修改，避免误改连接目标。
3. 重新连接 MCP，或新开本地聊天。个人地址适用于本机多个项目，插件更新后也会沿用。卸载插件后，这条用户连接仍可在 Codex 的 MCP 服务器设置中管理。UE 端的监听地址需单独设置。

`unreal-mcp` 负责连接编辑器；新增的 `unreal-mcp-settings` 只提供地址设置。若升级后未出现后者，重启 Codex 以刷新已安装插件；它不是 UE 编辑器插件。
本插件不会扫描任意端口来猜测连接，也不会把默认示例声称为自动发现的结果。

## 编译与保存

明确要求编译或已经授权的编译可以在范围内执行。仅要求分析、修改或修复，
不自动授权编译、Live Coding，以及间接触发编译的测试/脚本。
引擎工作流也遵循相同的授权范围。已获授权的操作无需重复确认。

## 来源与差异

上游：https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin
插件 0.1.6 同步了上游 3.1.2（`0e27bde2b55c5d3f6948532f4296aaa3654d8f4b`）的多编辑器指引。5.8 与 5.9 的调用差异另行对照 Epic 引擎文档和源码核实。完整来源见 [UPSTREAM.md](plugins/codex-unreal-engine-skills/UPSTREAM.md)。`upstream-changes.diff` 保留 0.1.1 制作时的差异。

## 项目结构与维护

| 路径 | 用途 |
| --- | --- |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | 本地 marketplace 入口。 |
| [`plugins/codex-unreal-engine-skills/`](plugins/codex-unreal-engine-skills/) | 可安装插件根目录，包含清单、连接配置、技能和许可证。 |
| [`AGENTS.md`](AGENTS.md) | 阅读顺序、版本同步和协作约定。 |
| [`Docs/CHANGELOG.md`](Docs/CHANGELOG.md) | 各版本的实际变更、验证结果与待验证事项。 |
| [`VALIDATION.json`](VALIDATION.json)、[`upstream-changes.diff`](upstream-changes.diff) | 0.1.1 制作时的历史验证与技能差异材料。 |

## 维护与反馈

本 Codex 适配版由 liuli-zsl 维护。安装或连接遇到问题，可在 [GitHub Issues](https://github.com/liuli-zsl/codex-unreal-engine-skills/issues) 反馈。

## 许可证

仓库和可安装插件均使用 MIT 许可证，保留 Epic Games 的原署名。[仓库许可证](LICENSE) · [随包许可证](plugins/codex-unreal-engine-skills/LICENSE) · [来源与适配说明](plugins/codex-unreal-engine-skills/UPSTREAM.md)
本项目为非官方适配版。
