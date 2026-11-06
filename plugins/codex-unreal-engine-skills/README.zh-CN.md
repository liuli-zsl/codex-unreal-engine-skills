# Unreal Engine Skills for Codex

当前版本：**0.1.4**。基于 Epic Games 的 Unreal Engine Skills for Claude Code 上游 3.1.1，面向本机 ChatGPT/Codex 会话；本包为非官方适配版。

## 包含的技能

- `unreal-mcp`：查询和操作正在运行的 UE 编辑器。
- `create-toolset`：开发或扩展 C++/Python MCP 工具。
- `unreal-skill`：创建或编辑 UE 项目/插件内的 Agent Skill。

连接声明见 [mcp.json](mcp.json)，技能位于 [skills/](skills/)。
随包地址 `http://127.0.0.1:8000/mcp` 是初次配置示例，使用时以目标编辑器实际地址和已有连接为准。
打开插件详情页 → **管理** → **unreal-mcp-settings（Unreal MCP 地址设置）**，直接在原生 **Unreal MCP 地址** 输入框填写完整 URL，按 Enter 或移开焦点保存。无需聊天或手动修改文件。需要 Python 3 和支持 `openai/settings` 的桌面版 Codex；UE 未启动时也能修改。个人设置写入前备份，重新连接或新开本机会话后使用。

插件标识为 `codex-unreal-engine-skills`，显示名称为 `Unreal Engine Skills for Codex`。
0.1.2 更新了源码命名。0.1.4 用原生设置替代 0.1.3 的聊天配置入口。Windows 上已通过真实 Codex 宿主验证扩展发现、读取、保存、回读、无效输入及配置保留；桌面点击与其他操作系统未验证。

## 验证状态

2026-10-27，现有 0.1.1 安装的三个技能和 MCP 工具已加载，实际只读查询选中 Actor 成功。
未验证全新安装、所有技能自动触发、编辑操作或编译。此说明的更新不代表已安装缓存已同步。

## 文档与来源

完整源码包的外层目录提供 [英文 README](../../README.md)、[中文说明](../../README.zh-CN.md)、
[协作约定](../../AGENTS.md) 和 [变更记录](../../CHANGELOG.md)。这些外层文档不会必然随单独插件安装保留。

独立插件内可查阅 [连接配置参考](skills/unreal-mcp/references/setup.md)、
[操作与排障参考](skills/unreal-mcp/references/operations.md)、[来源记录](UPSTREAM.md) 与 [MIT 许可证](LICENSE)。
