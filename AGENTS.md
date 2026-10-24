# AGENTS.md — FireworksLife（鱼腹）速通手册

> 新会话/新人 5 分钟跑起来所需的全部入口；细节以 `README.md` 为准。最后更新：2026-10-24。

## 这是什么

Astro 7 静态博客 + Netlify Functions/Blobs（评论/点赞/收藏）。源码在 `frontend/`，文章在 `frontend/src/content/blog/`（frontmatter 必填 `pubDate`，留空会被 build 拒绝）。

## 启动

```bash
cd frontend
npm install
npm run dev          # 默认自带 mock server(:4322)——评论/点赞/收藏本地可测
```

- `npm run dev:no-mock`：纯静态（互动功能自动走 localStorage 降级）
- `npm run reset-mock`：清空 mock 内存数据（评论/点赞/收藏归零；测试残留用它）

## 测试与验收（单条命令）

```bash
npm run verify       # = check:content（pubDate 护栏）+ node --test（契约测试）+ astro build
```

## 部署（唯一权威路径：Netlify）

- 根目录 `netlify.toml`：`cd frontend && npm install && npm run build`，publish = `frontend/dist`
- **前置（2026-10-24 状态：未完成）**：owner 的 Netlify 账号建站并接到本 repo（yufu.netlify.app / yufu.blog 均被第三方占用，域名待拍板）
- 函数：`frontend/netlify/functions/engagement.mjs`；线上 env 需配 `ADMIN_KEY`（manual 审核模式的 approve 通道），可选 `MODERATION_MODE=auto`
- 无 Docker 部署路径（`.dockerignore` 已移除，避免误导）

## 上线验收 checklist

- [ ] `curl 首页` 返回内容含"鱼腹"
- [ ] `/rss.xml` 200（item 数 ≥ 文章数）；`/sitemap-index.xml` 200
- [ ] `og:url` / `canonical` 与最终域名一致（`frontend/astro.config.mjs` 的 `site` 字段）
- [ ] 评论 API 响应 JSON 无 `clientId` 字段
- [ ] `/tags/<tag>/` 200（现有 AI/开发/工具/流程/思考 五个标签页）

## 常见坑

1. `pubDate` 留空 → build 直接拒（schema refine + prebuild 双护栏，别绕过）
2. 改生产函数行为 → 必须同步 `frontend/lib/engagement-shared.mjs`（mock 与生产共享同一份 sanitize/序列化，一处修两处生效；改单侧必然分叉）
3. `sitemap-index.xml` 在 `astro dev` 下 404 属正常——它是构建期产物，`npm run build && npm run preview` 才有
4. `data/*.db` 是本地 Blobs 落盘残留，`.gitignore` 已覆盖，勿提交
5. mock 是纯内存存储：重启或 `reset-mock` 即清零，别在里面存需要保留的东西
