---
title: "Beads和OpenSpec：AI代理为什么需要两套系统"
description: "任务追踪是个灾难。OpenSpec和Beads分别解决'想清楚'和'追踪执行'的问题，刚好互补。"
pubDate: 2026-03-30
category: "技术"
tags: ["AI", "Agent", "OpenSpec", "Beads", "任务管理"]
---

## 一个我观察到的痛点

AI代理越来越强，能写代码、能重构、能做复杂任务。但有个问题越来越明显：

**任务追踪是个灾难。**

- 你让AI做一个功能，它可能拆成10个子任务
- 你让它并行做，它可能搞混状态
- 你让它接手别人的任务，它可能不知道哪个已经完成了

传统的解决方案：
- AGENTS.md里写tasks.md——静态清单，没有状态管理
- GitHub上开issue——有状态，但没有依赖追踪
- Trello/Jira——不是为AI代理设计的

**没有一个是真正为AI代理设计的。**

---

## OpenSpec vs Beads

### OpenSpec：规范驱动开发

核心是Artifact链：

```
proposal.md → design.md → specs/*.md → tasks.md → 实现 → 归档
```

解决"怎么想清楚"的问题，但tasks.md是静态的checkbox清单。

### Beads：AI代理任务追踪器

核心是依赖图：

```
Epic (bd-xxx) → Task (bd-xxx.1) → Sub-task (bd-xxx.1.1)
```

解决"怎么追踪执行"的问题——Hash IDs、依赖关系、Compaction压缩。

---

## 核心发现

**OpenSpec和Beads解决的问题不重合，但刚好互补。**

| 维度 | OpenSpec | Beads |
|------|----------|-------|
| 解决什么问题 | "怎么想清楚" | "怎么追踪执行" |
| 状态管理 | 无 | 有 |
| 依赖追踪 | 无 | 有 |
| 多代理协作 | 单代理模式 | 天然支持 |

**OpenSpec有设计文档，但没有执行追踪。Beads有执行追踪，但没有设计文档。**

---

## 结合方案

OpenSpec负责"想清楚"，Beads负责"追踪执行"：

```
proposal.md → design.md → specs/*.md 
                                  ↓
                        Beads 任务追踪（bd-xxx）
                                  ↓
                        实现 → 归档
```

两者结合，才是AI代理的完整工作流。
