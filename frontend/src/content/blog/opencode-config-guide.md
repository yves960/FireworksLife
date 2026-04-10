---
title: "如何用 AI 代替我：第二章 - OpenCode 配置详解"
description: "拆解 OpenCode 配置——每个插件、每个参数、每个 Skill 的用法。"
pubDate: 2026-03-31
category: "技术"
tags: ["OpenCode", "AI", "配置"]
---

## 配置文件结构

OpenCode 的配置目录在 `~/.config/opencode/`：

```
~/.config/opencode/
├── opencode.json          # 主配置文件
├── opencode-arise.json    # Arise 插件配置
├── oh-my-opencode.json    # 主题插件配置
├── superpowers/           # Skills 和 Agents
│   ├── skills/            # 技能定义
│   ├── agents/            # Agent 定义
│   └── hooks/             # 钩子脚本
└── plugin/                # 插件软链接
```

## 主配置文件

```json
{
  "provider": { ... },
  "model": "minimax/MiniMax-M2.7",
  "small_model": "zhipuai-coding-plan/glm-4.7",
  "plugin": [
    "oh-my-opencode",
    "opencode-worktree",
    "opencode-supermemory",
    "opencode-browser",
    "opencode-pty",
    "opencode-arise"
  ],
  "lsp": { ... }
}
```

## 核心插件

- **oh-my-opencode**：主题和UI增强
- **opencode-worktree**：Git worktree 管理
- **opencode-supermemory**：记忆系统
- **opencode-browser**：浏览器自动化
- **opencode-pty**：终端集成
- **opencode-arise**：AI 任务编排

## provider：多模型配置

OpenCode 最强大的地方是 **provider-agnostic**——可以配置多个模型提供商，按需切换。
