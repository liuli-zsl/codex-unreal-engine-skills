# Unreal Engine Skills for Codex

当前版本：**0.1.3**。基于 Epic Games 的 Unreal Engine Skills for Claude Code 上游 3.1.1，面向本机 ChatGPT/Codex 会话；本包为非官方适配版。

## 包含的技能

- `unreal-mcp`：查询和操作正在运行的 UE 编辑器。
- `create-toolset`：开发或扩展 C++/Python MCP 工具。
- `unreal-skill`：创建或编辑 UE 项目/插件内的 Agent Skill。

连接声明见 [mcp.json](mcp.json)，技能位于 [skills/](skills/)。
随包地址 `http://127.0.0.1:8000/mcp` 是初次配置示例，使用时以目标编辑器实际地址和已有连接为准。
在插件详情页点 **在聊天中试用（Try in chat）**，发送首条建议 **配置 Unreal MCP 地址**，按提示输入 UE 编辑器的完整地址。个人设置保存在 Codex 用户配置里，重新连接或新开本机会话后使用。

插件标识为 `codex-unreal-engine-skills`，显示名称为 `Unreal Engine Skills for Codex`。
0.1.2 更新了源码命名。0.1.3 在隔离的 Codex 用户配置中验证了安装和地址切换。

## 验证状态

2026-10-27，现有 0.1.1 安装的三个技能和 MCP 工具已加载，实际只读查询选中 Actor 成功。
未验证全新安装、所有技能自动触发、编辑操作或编译。此说明的更新不代表已安装缓存已同步。

## 文档与来源

完整源码包的外层目录提供 [英文 README](../../README.md)、[中文说明](../../README.zh-CN.md)、
[协作约定](../../AGENTS.md) 和 [变更记录](../../CHANGELOG.md)。这些外层文档不会必然随单独插件安装保留。

独立插件内可查阅 [连接配置参考](skills/unreal-mcp/references/setup.md)、
[操作与排障参考](skills/unreal-mcp/references/operations.md)、[来源记录](UPSTREAM.md) 与 [MIT 许可证](LICENSE)。
