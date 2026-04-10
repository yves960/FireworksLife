---
title: "Claude Code 源码架构分析"
description: "基于2026-03-31泄露的源码快照，分析Claude Code的整体架构。"
pubDate: 2026-03-31
category: "技术"
tags: ["Claude", "AI编程", "源码分析"]
---

## 整体架构

```
CLI Entry (main.tsx)
        │
        ▼
QueryEngine.ts (LLM API调用/流式响应/Tool-Call循环)
        │
        ├── Tools (40+ 工具)
        ├── Commands (50+ 命令)
        └── Services (外部服务)
```

## 核心组件

### Tool 系统

每个 Tool 是一个自包含模块，定义：

```typescript
interface Tool {
  name: string;        // 工具名称
  inputSchema: Zod;   // 输入参数校验
  handler: Function;   // 实际执行逻辑
}
```

### QueryEngine

LLM API 调用入口，处理：
- 流式响应解析
- Tool Call 循环控制
- 上下文窗口管理

### Commands

50+ 内置命令，覆盖：
- 文件操作（read, write, edit, glob）
- Git 操作（commit, branch, diff）
- 开发流程（test, build, deploy）

## 设计亮点

1. **Zod Schema 验证**：所有工具输入都有类型校验
2. **流式优先**：原生支持 Server-Sent Events
3. **模块化 Tool**：新增工具只需实现接口
4. **Command 模式**：命令行交互标准化
