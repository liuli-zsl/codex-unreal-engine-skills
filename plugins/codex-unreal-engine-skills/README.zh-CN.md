# Unreal Engine Skills for Codex

当前版本 **0.1.8**。基于 Epic Games 的 Unreal Engine Skills for Claude Code 上游 3.1.2，面向本机 ChatGPT/Codex 会话。本包为非官方适配版。

插件按编辑器提供的工具选择 UE 5.8 或 5.9 Preview 查询流程。多个实例并行时，请核对各自的端口、进程和工程目录。

## 引擎工作流与桌面入口

| 来源 | UE 5.8 | UE 5.9 |
| --- | --- | --- |
| Epic 为 Claude Code 提供的 GitHub 技能 | `unreal-mcp` 操作编辑器，`create-toolset` 开发工具，`unreal-skill` 编写引擎技能。 | 同样三项，引擎另支持 Markdown 技能。 |
| UE 安装自带的工作流 | [21 项共用技能](skills/unreal-engine-workflows/references/shared.csv)，包括蓝图、光照、材质、Niagara、Dataflow、布料转换和 PCG 资产。 | 共用 21 项，加上 [57 项 5.9 工作流](skills/unreal-engine-workflows/references/ue5.9.csv)，覆盖编辑器、UI、Sequencer、音频、渲染、变形、工具链、PCG 和 Wasm。 |
| UE 5.9 宿主 | — | [Canvas 和 Assistant](skills/unreal-engine-workflows/references/canvas-assistant.md)。Canvas 有独立技能库及扩展编写技能，Assistant 使用编辑器注册表。 |

本项目编写的 [`unreal-engine-workflows`](skills/unreal-engine-workflows/SKILL.md) 是第四个桌面入口。先核对目标引擎版本，再按当前编辑器返回的路径取完整指令。编辑器关闭时，按版本查随包指引或读取对应安装的文本定义。蓝图资产与项目动态正文通过在线编辑器读取。

连接声明见 [mcp.json](mcp.json)，技能位于 [skills/](skills/)。
随包地址 `http://127.0.0.1:8000/mcp` 是初次配置示例，使用时以目标编辑器实际地址和已有连接为准。
打开插件详情页 → **设置 → Unreal Editor 连接**，分别填写 **IP**、**URL 路径**、**端口号**，默认值依次为 `127.0.0.1`、`/mcp`、`8000`。按 Enter 或移开焦点保存；错误输入不会写入。端口范围 1–65535，路径以 `/` 开头。点击 **恢复默认值** 一次保存默认 HTTP 地址，重新打开页面刷新显示。普通修改保留已有 HTTPS 协议；升级不覆盖自定义地址。无需聊天或手动修改文件。需要 Python 3 和支持 `openai/settings` 的桌面版 Codex；UE 未启动时也能修改。个人设置写入前备份，重新连接或新开本机会话后使用。

插件标识为 `codex-unreal-engine-skills`，显示名称为 `Unreal Engine Skills for Codex`。

## 验证状态

2026-11-26 在 Windows 独立 Codex 配置中安装并启用了 0.1.8。已在 UE 5.8.4 和 5.9.0 核对 21 项和 78 项对应来源。5.8.4 临时工程的无界面 Commandlet 通过 MCP 返回蓝图基础正文。5.9 编辑器通过 MCP 返回蓝图基础、PCG 图生成资产和日志分析正文。

## 文档与来源

GitHub 提供完整的安装指南与维护说明。[英文 README](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.md) · [中文说明](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.zh-CN.md) · [协作约定](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/AGENTS.md)

本版本源码的逐版记录位于 `Docs/CHANGELOG.md`。在 GitHub 中文首页的“项目结构与维护”可打开公开分支的变更记录。[变更记录入口](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.zh-CN.md#项目结构与维护)

独立插件内可查阅 [连接配置参考](skills/unreal-mcp/references/setup.md)、
[操作与排障参考](skills/unreal-mcp/references/operations.md)、[来源记录](UPSTREAM.md) 与 [MIT 许可证](LICENSE)。
