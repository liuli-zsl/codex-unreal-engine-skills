# Unreal Engine Skills for Codex

当前版本 **0.1.6**。基于 Epic Games 的 Unreal Engine Skills for Claude Code 上游 3.1.2，面向本机 ChatGPT/Codex 会话。本包为非官方适配版。

插件按编辑器提供的工具选择 UE 5.8 或 5.9 Preview 查询流程。多个实例并行时，请核对各自的端口、进程和工程目录。

## 包含的技能

- `unreal-mcp`：查询和操作正在运行的 UE 编辑器。
- `create-toolset`：开发或扩展 C++/Python MCP 工具。
- `unreal-skill`：创建或编辑 UE 项目/插件内的 Agent Skill。

连接声明见 [mcp.json](mcp.json)，技能位于 [skills/](skills/)。
随包地址 `http://127.0.0.1:8000/mcp` 是初次配置示例，使用时以目标编辑器实际地址和已有连接为准。
打开插件详情页 → **设置 → Unreal Editor 连接**，分别填写 **IP**、**URL 路径**、**端口号**，默认值依次为 `127.0.0.1`、`/mcp`、`8000`。按 Enter 或移开焦点保存；错误输入不会写入。端口范围 1–65535，路径以 `/` 开头。点击 **恢复默认值** 一次保存默认 HTTP 地址，重新打开页面刷新显示。普通修改保留已有 HTTPS 协议；升级不覆盖自定义地址。无需聊天或手动修改文件。需要 Python 3 和支持 `openai/settings` 的桌面版 Codex；UE 未启动时也能修改。个人设置写入前备份，重新连接或新开本机会话后使用。

插件标识为 `codex-unreal-engine-skills`，显示名称为 `Unreal Engine Skills for Codex`。
0.1.2 更新了源码命名，0.1.4 改为原生设置，0.1.5 拆分三项并增加恢复默认值。Windows 上已通过真实 Codex 宿主验证独立读写、重置、回读、非法输入、备份及配置保留；新版表单点击与其他操作系统未验证。

## 验证状态

0.1.6 在 Windows 上使用 Codex CLI `0.169.0-alpha.11.1` 验证。2026-11-17 从本地 marketplace 升级并保留已有连接地址，在 UE 5.9 Preview 实际调用 `GetSelectedActors` 成功，返回空列表。2026-11-18 使用空白配置从公开 GitHub marketplace 安装并确认启用。UE 5.8.4 已对照引擎源码和配置核查，编辑器只读调用待验。

2026-10-27，现有 0.1.1 安装的三个技能和 MCP 工具已加载，实际只读查询选中 Actor 成功。
该次 0.1.1 验证范围仅限已有安装的加载与只读查询。

## 文档与来源

完整源码包的外层目录提供 [英文 README](../../README.md)、[中文说明](../../README.zh-CN.md)、
[协作约定](../../AGENTS.md) 和 [变更记录](../../CHANGELOG.md)。这些外层文档不会必然随单独插件安装保留。

独立插件内可查阅 [连接配置参考](skills/unreal-mcp/references/setup.md)、
[操作与排障参考](skills/unreal-mcp/references/operations.md)、[来源记录](UPSTREAM.md) 与 [MIT 许可证](LICENSE)。
