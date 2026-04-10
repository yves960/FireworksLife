---
title: "Agent Memory 深度解析"
description: "AI Agent 是如何记忆的？Session、Memory、Knowledge 三层架构详解。"
pubDate: 2026-03-30
category: "技术"
tags: ["AI", "Agent", "Memory"]
---

# Agent Memory 深度解析

## 为什么 Memory 对 Agent 很重要？

人类对话之所以连贯，是因为我们有记忆。AI Agent 也一样——没有 Memory，每次对话都是全新的开始。

## 三层 Memory 架构

### 1. Session Memory（会话记忆）
当前对话的上下文，随会话结束而消失。

```python
session = {
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"}
    ]
}
```

### 2. Short-term Memory（短期记忆）
跨会话但有时效性的信息，比如：
- 用户最近的偏好
- 进行中的任务状态
- 刚学习到的新知识

### 3. Long-term Memory（长期记忆）
持久化存储，类似人类的"知识库"：
- 用户背景信息
- 技能知识
- 历史交互总结

## 存储方案对比

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| SQLite | 小规模 | 简单、无依赖 | 并发差 |
| PostgreSQL | 生产环境 | 强大、可靠 | 需要运维 |
| Chroma | 向量检索 | AI 原生 | 复杂 |
| Redis | 缓存 | 超快 | 需额外服务 |

## 实践建议

1. **从简单开始**：先用 SQLite，满足不了再升级
2. **分层存储**：Session 用内存，Long-term 用数据库
3. **定期压缩**：总结历史对话，避免 context 膨胀
4. **隐私优先**：敏感信息加密存储

## 总结

Memory 是 Agent 的核心能力之一。设计好的 Memory 系统，让 AI 真正"懂"你。
