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

## Scripts

```bash
cd frontend
npm run dev            # 默认开发入口：mock server（:4322）+ astro dev（:4321），评论/点赞/收藏本地可测
npm run dev:no-mock    # 仅 astro dev（Netlify Functions 本地 404）
npm run dev:mock       # 等价于 dev
npm run mock           # 仅启动 mock server
npm run check:content  # 内容护栏：文章 frontmatter 的 pubDate 不得为空
npm run build          # check:content + 生产构建（输出 frontend/dist）
npm run preview        # 预览构建产物
```

仓库根目录 `scripts/sync-articles.sh` 为文章同步脚本（CI 使用）。

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
├── memory/                 # 产品创意笔记（入库保留）
├── openspec/               # OpenSpec 规格
├── scripts/                # 文章同步等源码脚本（入库保留）
├── netlify.toml
└── README.md

> 约定：`frontend/scripts/mock-server.mjs` 与根 `scripts/` 为被 package.json / CI 引用的源码脚本，保持入库；`.claude/`、`.astro/`、`.venv/`、`node_modules/`、`dist/` 等运行时产物由 `.gitignore` 排除。
```
