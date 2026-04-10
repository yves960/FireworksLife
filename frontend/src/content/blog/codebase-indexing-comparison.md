---
title: "Claude Code的代码检索之争：精准的代价"
description: "为什么Claude Code不用索引？Cursor和Claude Code的两种代码检索方案对比。"
pubDate: 2026-03-30
category: "技术"
tags: ["Claude", "Cursor", "AI编程", "代码检索"]
---

## 一个真实的故事

一个工程师让Claude Code帮忙找bug。

Claude Code开始了"侦探工作"：反复执行`grep`命令，猜测可能的关键词，不断读取文件。5分钟后，它才终于定位到问题文件。

**真正的问题：这5分钟里，Claude Code读取了大量文件，只有10行代码和bug相关，其他99%都是无关代码。**

这不是个例。这是**代码检索问题**。

---

## "grep就够了"——真的够吗？

Claude Code的工程师说过：**代码检索仅靠grep文本搜索就能搞定。**

这句话在社区引发了激烈争论。

支持的人说，编程需要高度精准的操作，embedding在代码检索方面表现不够精准。

反对的人说，传统grep方案召回率低，还会检索出大量不相关的内容。

**两种说法都对，但说的是不同的场景。**

---

## 两种设计哲学

要理解为什么Claude Code不用索引，得先理解它的设计哲学。

**Cursor在问"怎么让AI更好地适应人的工作流"**

→ 维护本地语义索引，AI知道你写`user.service.ts`时，`auth.service.ts`里有`validateToken`

**Claude Code在问"怎么让AI成为一个独立的工作者"**

→ 背靠1M token大上下文，用Context Compact自动压缩，用Checkpoint保存进度

**哪种更好？取决于你想要什么。**

---

## 但大代码库确实有问题

在同等召回率的情况下，使用向量检索可以**减少40%以上的token消耗**。

这意味着：
- 有限的token预算里，向量检索效果更好
- 10万行、100万行代码库，纯grep方案效率低下

**没有完美方案，只有取舍。**

- Cursor：精准检索，工程复杂度高
- Claude Code：简单可靠，大代码库效率低
