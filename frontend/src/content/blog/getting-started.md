---
title: "开始使用 Astro"
date: "2026-04-09"
excerpt: "快速搭建一个暗色主题博客的指南。"
---

## 为什么选 Astro

Astro 是现代静态站点生成器，核心优势：

1. **零 JS 默认** — 页面不加载任何 JavaScript
2. **内容优先** — 天然支持 Markdown
3. **快速** — 构建飞快，页面加载秒开

## 暗色主题设计

这个博客用了：

- 深紫渐变背景 `#0a0a1a → #1a0a2e → #0a1a2e`
- 紫色主色调 `#8b5cf6`
- Space Grotesk 字体
- 粒子星空动效

## 写文章

在 `src/content/blog/` 下新建 `.md` 文件，加上 frontmatter：

```yaml
---
title: "文章标题"
date: "2026-04-10"
excerpt: "简介"
---
```

就这么简单。
