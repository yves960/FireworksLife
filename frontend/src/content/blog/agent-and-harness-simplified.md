---
title: "Agent和Harness：我为什么说这不是两个概念，而是一套世界观"
description: "从AI编程的困惑出发，理解Agent和Harness的本质区别。"
pubDate: 2026-03-30
category: "技术"
tags: ["AI", "Agent", "Harness"]
---

## 从一个困惑开始

刚接触AI编程的时候，我有一个困惑：

**为什么有些人叫它"AI Agent"，有些人叫它"AI助手"，还有些人根本不叫它名字，就说"用AI写代码"？**

后来我明白了，这不只是叫法的问题，而是**理解AI的方式不同**。

有些人把AI当成一个工具，像锤子、螺丝刀，拿来用就行。

有些人把AI当成一个员工，给它任务、给它资源、给它边界。

**这两种理解，对应着两个概念：Agent和Harness。**

---

## Agent：不是框架，是模型本身

我看过很多文章把Agent说得很复杂——框架、提示词链、工作流编排、决策树……

**但learn-claude-code项目说得很清楚：Agent就是模型本身。**

不是框架，不是提示词链，不是工作流。**Agent是一个神经网络**——经过数十亿次训练，学会了感知、推理、行动。

这听起来很抽象，但看看历史就明白了：

| 里程碑 | 做了什么 |
|--------|----------|
| DeepMind DQN | 一个神经网络打7款Atari游戏，超越人类 |
| OpenAI Five | 五个神经网络打Dota 2，击败世界冠军OG |
| AlphaStar | 一个神经网络打星际争霸II，达到宗师段位 |
| 腾讯绝悟 | 一个神经网络打王者荣耀，击败职业选手 |

注意到了吗？**每一个里程碑，核心都是神经网络本身**，不是外面包的那层代码。

**Agency（智能体能力）是学出来的，不是编出来的。**

你可以用if-else串起一个工作流，让LLM在不同节点做文本补全。但这不是Agent，这是"有着宏大妄想的shell脚本"。

真正的Agent，它的决策能力来自模型本身，不是外面的规则。

---

## Harness：给智能体一个栖居的世界

如果Agent是"脑"，那Harness是什么？

**Harness是Agent在特定领域工作所需要的一切环境。**

```
Harness = Tools + Knowledge + Observation + Action + Permissions
```

- **Tools**：文件读写、Shell、网络、浏览器——给它一双手
- **Knowledge**：产品文档、API规范、风格指南——给它领域知识
- **Observation**：git diff、错误日志、浏览器状态——给它眼睛
- **Action**：CLI命令、API调用、UI交互——让它能做事
- **Permissions**：沙箱隔离、审批流程、信任边界——给它边界

**模型是驾驶者，Harness是载具。**

编程Agent的Harness是IDE、终端、文件系统。

农业Agent的Harness是传感器、灌溉控制、气象数据。

酒店Agent的Harness是预订系统、客户沟通渠道、设施管理API。

**Agent做决策，Harness执行。Agent做推理，Harness提供上下文。**

---

## 我理解的Agent Pattern

learn-claude-code里有一张图，我看了很久：

```
User --> messages[] --> LLM (Agent) --> response
                              |
                              v
                        Tool Calls
                              |
                              v
                          Harness
```

用户发消息给Agent，Agent思考后调用工具，工具来自Harness。

**Harness给Agent赋能，Agent利用Harness行动。**

这让我想起一个比喻：

- LLM是驾驶员
- Agent是驾驶技术（能力）
- Harness是汽车

你可以换不同的车（不同的harness），但驾驶员还是你。

**你不能教一个不会开车的人开好车，但你可以给他一辆更好的车。**

---

## 结论

- **Agent**是模型的决策能力，是学出来的
- **Harness**是Agent执行的环境，是构建出来的
- 好的Harness让Agent发挥全部潜力
- 差的Harness让强大的Agent寸步难行

这就是为什么，换一套环境，同一个模型的表现可能天差地别。
