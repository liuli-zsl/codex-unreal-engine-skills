# Unreal Engine Skills for Codex

[English](README.md) | 简体中文

当前插件版本：**0.1.3**。协作约定见 [AGENTS.md](AGENTS.md)，变更与验证记录见 [CHANGELOG.md](CHANGELOG.md)。

这是基于 Epic Games 官方技能仓库制作的通用桌面适配版，不是 Epic/OpenAI 官方发行版。
保留三个技能及官方工具开发示例，目标是 ChatGPT 统一桌面端的本机会话。

## 包含什么

- `unreal-mcp`：查询和操作正在运行的 UE 编辑器。
- `create-toolset`：开发或扩展 C++/Python MCP 工具。
- `unreal-skill`：创建或编辑 UE 项目/插件内的 Agent Skill。
- 首次配置示例：`http://127.0.0.1:8000/mcp`（UE 官方默认值，可修改）。
- 已有连接和编辑器实际设置优先，不包含特定用户的端口、工程路径或补丁版本预设。
- 原始 MIT 许可证、上游版本记录、可检查的源码，以及本地插件目录。

## 先看验证范围

0.1.3 已在隔离的桌面版 Codex 用户配置中验证安装、个人地址保存与重新读取。本次没有在桌面界面点击入口或连接实际 UE 工程。

2026-10-27 已确认现有 0.1.1 安装加载了三个技能和 Unreal MCP 工具。
文档修改前，源码插件目录与已安装缓存内容一致；实际调用 `list_toolsets`、
`describe_toolset` 和 `GetSelectedActors` 成功，返回一个选中 Actor。

这证明该次现有安装的只读连接可用；未验证全新安装、所有技能自动触发、资产修改、
UE 编译或其他平台。本目录是源码整理副本，修改文档不等于已更新已安装缓存。
`VALIDATION.json` 保留制作时的历史检查结果，当前验证记录以 [CHANGELOG.md](CHANGELOG.md) 为准。

## 从旧名称迁移

0.1.2 将插件标识从 `unreal-engine-chatgpt-desktop` 改为 `codex-unreal-engine-skills`，
显示名称改为 `Unreal Engine Skills for Codex`；本地 marketplace 标识从
`ue-mcp-desktop-local` 改为 `codex-unreal-engine-skills-local`。
源码根目录和可安装插件子目录均使用新名称。

现有 0.1.1 安装仍保留原标识与缓存，源码改名不会自动更新它。
升级时从新目录安装并单独验证连接。
MCP 服务键仍为 `unreal-mcp`，安装时注意避免无意同时启用两份插件连接。

## 本地安装方式

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

打开插件详情页，点 **在聊天中试用（Try in chat）**，发送首条建议 **配置 Unreal MCP 地址**。如果客户端没有显示建议，在本机会话里选中插件并发送同一句话即可。

1. Codex 会显示当前使用的地址。输入要保存的完整地址，例如 `http://127.0.0.1:9000/mcp`。
2. 插件使用 Python 3 和桌面版 Codex，只更新个人设置 `mcp_servers.unreal-mcp.url`，写入前备份已有配置，保存后回读有效地址。已配置认证或使用其他传输方式的同名连接，请在 Codex 的 MCP 服务器设置中处理。
3. 重新连接 MCP，或新开本地聊天。个人地址适用于本机多个项目，插件更新后也会沿用。卸载插件后，这条用户连接仍可在 Codex 的 MCP 服务器设置中管理。UE 端的监听地址需单独设置。
本插件不会扫描任意端口来猜测连接，也不会把默认示例声称为自动发现的结果。

## 编译与保存

明确要求编译或已经授权的编译可以在范围内执行。仅要求分析、修改或修复，
不自动授权编译、Live Coding，以及间接触发编译的测试/脚本。
该规则放在三个技能入口中。用户当前指令优先，已授权范围内不重复确认。

## 来源与差异

上游：https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin
上游快照：`a6aa73ada02a9fb1f5415bec491f9942c519b297`，原插件清单版本 3.1.1。
当前适配版：0.1.3。完整来源说明见插件内 `UPSTREAM.md`；逐文件文本差异见
本包 `upstream-changes.diff`。技能脚本没有增加额外编译执行器。

## 项目结构与维护

| 路径 | 用途 |
| --- | --- |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | 本地 marketplace 入口。 |
| [`plugins/codex-unreal-engine-skills/`](plugins/codex-unreal-engine-skills/) | 可安装插件根目录，包含清单、连接配置、技能和许可证。 |
| [`AGENTS.md`](AGENTS.md) | 阅读顺序、版本同步和协作约定。 |
| [`CHANGELOG.md`](CHANGELOG.md) | 实际变更、验证证据与未验证范围。 |
| [`VALIDATION.json`](VALIDATION.json)、[`upstream-changes.diff`](upstream-changes.diff) | 0.1.1 制作时的历史验证与技能差异材料。 |

后续独立修改按 AGENTS.md 同步版本和文档。

## 许可证

沿用 [MIT 许可证](plugins/codex-unreal-engine-skills/LICENSE) 和 Epic Games 原署名。
完整来源与适配说明见 [UPSTREAM.md](plugins/codex-unreal-engine-skills/UPSTREAM.md)。
本项目为非官方适配版。
