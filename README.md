# 鱼腹

一个基于 `Astro + Netlify` 的个人博客，当前支持：

- Markdown / MDX 写作
- Netlify Functions + Blobs 驱动的评论、点赞、收藏
- 高视觉强度的首页、文章页和吉祥物交互

## 技术栈

- `Astro`
- `@astrojs/mdx`
- `Netlify Functions`
- `@netlify/blobs`

## 本地开发

```bash
cd frontend
npm install
npm run dev
```

默认开发地址：

- 前端：`http://localhost:4321`

## 构建

```bash
cd frontend
npm run build
```

## 部署

仓库根目录已经配置了 `netlify.toml`，Netlify 会：

- 构建 `frontend`
- 发布 `frontend/dist`
- 使用 `frontend/netlify/functions` 作为函数目录

评论、点赞、收藏依赖 Netlify 平台运行时提供的 Functions / Blobs 环境。

## 项目结构

```text
.
├── frontend/
│   ├── netlify/functions/   # Netlify Functions
│   ├── public/
│   ├── src/
│   │   ├── content/blog/    # 博客文章
│   │   ├── layouts/
│   │   └── pages/
│   ├── astro.config.mjs
│   └── package.json
├── netlify.toml
└── README.md
```
