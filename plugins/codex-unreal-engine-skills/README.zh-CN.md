# Unreal Engine Skills for Codex

当前版本 **0.1.7**。基于 Epic Games 的 Unreal Engine Skills for Claude Code 上游 3.1.2，面向本机 ChatGPT/Codex 会话。本包为非官方适配版。

插件按编辑器提供的工具选择 UE 5.8 或 5.9 Preview 查询流程。多个实例并行时，请核对各自的端口、进程和工程目录。

## 包含的技能

- `unreal-mcp`：查询和操作正在运行的 UE 编辑器。
- `create-toolset`：开发或扩展 C++/Python MCP 工具。
- `unreal-skill`：创建或编辑 UE 项目/插件内的 Agent Skill。

连接声明见 [mcp.json](mcp.json)，技能位于 [skills/](skills/)。
随包地址 `http://127.0.0.1:8000/mcp` 是初次配置示例，使用时以目标编辑器实际地址和已有连接为准。
打开插件详情页 → **设置 → Unreal Editor 连接**，分别填写 **IP**、**URL 路径**、**端口号**，默认值依次为 `127.0.0.1`、`/mcp`、`8000`。按 Enter 或移开焦点保存；错误输入不会写入。端口范围 1–65535，路径以 `/` 开头。点击 **恢复默认值** 一次保存默认 HTTP 地址，重新打开页面刷新显示。普通修改保留已有 HTTPS 协议；升级不覆盖自定义地址。无需聊天或手动修改文件。需要 Python 3 和支持 `openai/settings` 的桌面版 Codex；UE 未启动时也能修改。个人设置写入前备份，重新连接或新开本机会话后使用。

插件标识为 `codex-unreal-engine-skills`，显示名称为 `Unreal Engine Skills for Codex`。

## 验证状态

2026-11-26 在 Windows 空白 Codex 配置中从本地 marketplace 安装并启用了 0.1.7，15 个安装文件均与源码一致。

2026-11-17 使用插件 0.1.6 在 UE 5.9 Preview 编辑器中调用 `GetSelectedActors` 成功，返回空列表。UE 5.8.4 已核对引擎源码和配置，编辑器只读调用仍待验证。

## 文档与来源

GitHub 提供完整的安装指南与维护说明。[英文 README](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.md) · [中文说明](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.zh-CN.md) · [协作约定](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/AGENTS.md)

本版本源码的逐版记录位于 `Docs/CHANGELOG.md`。在 GitHub 中文首页的“项目结构与维护”可打开公开分支的变更记录。[变更记录入口](https://github.com/liuli-zsl/codex-unreal-engine-skills/blob/main/README.zh-CN.md#项目结构与维护)

独立插件内可查阅 [连接配置参考](skills/unreal-mcp/references/setup.md)、
[操作与排障参考](skills/unreal-mcp/references/operations.md)、[来源记录](UPSTREAM.md) 与 [MIT 许可证](LICENSE)。
