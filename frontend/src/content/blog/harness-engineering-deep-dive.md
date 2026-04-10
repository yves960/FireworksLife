---
title: "Harness Engineering：一个被忽视的真相"
description: "同一个模型，换一套运行环境，成功率从42%跳到78%。Harness才是AI编程的关键。"
pubDate: 2026-03-30
category: "技术"
tags: ["AI", "Harness", "Agent", "编程"]
---

## 从一个数字说起

**同一个模型，换一套运行环境，编程基准的成功率就从42%跳到了78%。**

这个数据只有一个变量变了：模型外面包裹的那层"壳"。模型没换，数据没换，提示词也没换，只是改了壳，性能翻了将近一倍。

**这层壳，现在有了一个正式的名字：Harness。**

LangChain 用同一个模型，只改 Harness，Terminal Bench 2.0 的成绩从 52.8% 升到 66.5%。排名从三十名开外直接冲进前五。

**Harness 带来的提升，相当于换了一代模型。**

---

## 三层进化

**2022-2024：Prompt Engineering**

研究的是怎么写好一条指令。few-shot、chain-of-thought、角色扮演——打磨"一次性的输入"。

**2025：Context Engineering**

风向变了。你得为模型动态构建整个上下文环境——相关文件、历史对话、工具定义，知识库检索结果。

**2026：Harness Engineering**

它来了：

- Prompt Engineering = 教你怎么写一封好邮件
- Context Engineering = 教你怎么把相关附件都带上
- Harness Engineering = 教你怎么搭建整个办公室

**约束、反馈循环、架构规则、工具链、生命周期管理，以及对抗熵增的持续治理。**

---

## 核心洞见

OpenAI 的核心工程师 Ryan Lopopolo 写下了一句总结：

> **"Agent不难，Harness才难。"**

3名工程师，5个月，1500个PR，100万行代码，人类一行代码都没写。那些工程师在干什么？

**从"砌砖"变成了"设计建筑规范"。**
