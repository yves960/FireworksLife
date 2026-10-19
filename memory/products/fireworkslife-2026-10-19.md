# 📦 FireworksLife（鱼腹） - 体验报告

**体验人：** 蔚（Director）
**体验日期：** 2026-10-19
**体验环境：** 本地 dev（astro dev + mock server，端口 4321/4322）
**最近提交：** 2026-10-16（修债中，P1 已清，Netlify 域名阻塞待 owner 接线）
**结论：** 主体可用、视觉到位，但后端 API 一致性有 P1 隐患，UX 细节有 3 处可打磨。

---

## ✅ 优点

1. **视觉与品牌统一性很强** — 首页 hero 把"AI 中枢"概念落到「Signal Core」徽章上（芯片核心 + 环形扫描 + 节点连线 + 数据轨道），与"鱼腹"主题反差形成记忆点；`page-aurora` 背景、cursor-glow 跟随、pet sprite 表情切换都到位，沉浸感高于一般 Astro 博客。
2. **首页信息架构合理** — Hero（最新/置顶）→ Content Index（分类 + 标签 + 搜索）→ Saved Signals（本地收藏）→ 文章卡片网格，单页覆盖 80% 任务；置顶徽章 `★ 置顶` 显著、Latest Signal 与日期分行不挤。
3. **文章页阅读体验完善** — 顶栏 reading-progress 滚动条、右侧 Reading Brief 面板（阅读时长/字数/栏目 + 自动生成的 TOC 章节锚点）、文章底部 engagement-bar（点赞/收藏按钮 + 计数），骨架已经够"专业博客"。
4. **Netlify 端互动闭环可用** — 点赞、收藏、评论都跑通；评论走 auto moderation 立即返回（本次成功提交"体验者"评论并出现在 stats 中）；clientId 走 header 干净不污染 URL。
5. **404 有品牌化设计** — "这条鱼游走了"配 404 大字 + 鱼主题，气质没塌。
6. **mock-server 设计诚实** — README 明确告知"astro dev 下 sitemap-index.xml 404 属正常"、并提供 `dev:no-mock` 避开 Netlify Functions 缺失，文档先行做得好。
7. **首页置顶逻辑** — pinnedPost 优先于最新，置顶徽章与 Latest Signal 同行展示，业务语义对。

## ❌ 问题

### P1 — 后端 API 一致性
1. **Favorites 接口语义错乱**（mock-server.mjs）：`action=favorites` GET 既要 `slug` 也要 `clientId` 是错误的——favorites 应该是**按 client 列出**而不是按 post。本地调用时 GET 直接返回 `{"error":"缺少 slug"}`，前端如果想"拉取我所有收藏"会被这条错误堵住。
2. **POST 与 GET 参数风格不统一** — 同一个 engagement 端点，有的 action 走 query string（`?slug=`），有的走 JSON body，还有的读 header（`x-client-id`）。前端调用方需要为不同 action 切三种风格，错一个就 400 缺字段。
3. **缺少客户端标识时的失败恢复** — 如果 `localStorage` 里的 clientId 被清空，所有写操作（like/favorite/comment）立刻 400，UI 没有"刷新即恢复"或"自动重生 clientId"的兜底。

### P2 — UX 细节
4. **首页 Tags 折叠到「subtagExtra」hidden 里** — 5 个标签一次性全展开看着拥挤，但"更多标签"的隐藏折叠平时不展开，初次访问不知道还有更多，体验不到。
5. **Search 没有键盘快捷键** — `/` 直接聚焦搜索框是博客标配；当前只能用鼠标点。
6. **「我的收藏」入口在 nav 写的是 `/#favoritesShell` 锚点跳首页** — 但 favoritesShell 在首页的搜索/分类下面，肉眼找不到的话会以为没生效；nav 也没"已收藏 N 篇"的角标提示。
7. **engagement-bar 按钮在文章首屏折叠栏里** — 用户阅读正文时按钮要滚回顶部才能交互，缺少 sticky 浮动栏。
8. **404 页面有鱼主题但缺引导** — 没有"回到首页"或"看最新文章"的明显 CTA，只靠浏览器返回。
9. **Pinned post 是 4/4，但 4/13、4/10 的更新文章才是真正的"最新"** — `★ 置顶` + `Latest Signal` 双重标签会让人以为置顶 = 最新。建议：置顶时改为 `★ 置顶精选`，Latest Signal 仍指真正最新。
10. **关于页 (about.astro 4103B) 几乎纯静态** — 没有作者近期动态、没有"最近在写什么"的回链，访客看完 about 没有任何下一步引导。

### P3 — 卫生
11. `.astro/`、`dist/`、`node_modules/` 已在 .gitignore ✓。
12. 仓库根 `package.json` 缺失（仅 frontend 有），单仓 root 安装提示弱。
13. `data/` 目录有内容但 README 没说明用途，新人 onboarding 盲区。

## 💡 优化建议（按优先级）

1. **修 favorites 接口语义（艾克排 P1，本周内）**
   - `action=favorites` 的 GET 应只需 `x-client-id` 即可返回该 client 全部收藏列表，不要再校验 `slug`。
   - 统一所有 action 的参数风格：要么全 query string、要么全 JSON body + header；clientId 统一走 header。
   - 加幂等：clientId 为空时自动生成 UUID 写回 localStorage，避免 400 中断体验。

2. **engagement-bar 改成 sticky 浮动栏（艾克排 P2）**
   - 点赞/收藏按钮做成右下角悬浮组件，scroll 后仍然可点；评论锚点跳到文章末尾的评论区。
   - 顺便加一个评论数显示，让用户知道有互动。

3. **置顶与最新信号的标签语义分离（艾克排 P2）**
   - 置顶时 featured-card 的 topline 改为：`★ 置顶精选` / `Latest Signal` 互斥显示。
   - 或：置顶时不抢 Latest Signal 标签，改为"Editor's Pick"独立标识。

4. **加 `/` 搜索快捷键 + 角标（艾克排 P3）**
   - 全局 keydown 监听 `/` 聚焦 searchInput；nav 收藏入口带 "🔖 收藏 (3)" 角标，数字从 favoritesShell 同步。
   - 关于页加"最近文章"回链（取最近 3 篇），提升页内流转。

5. **关于页补"个人脉搏"小模块（艾克排 P3）**
   - 显示最近 commit 时间、最近一篇文章、最近一条评论预览，让关于页从静态介绍变成活的入口。

## 🚀 新功能想法

- **暗色/亮色主题切换**：当前 visual 重，但只看得到一种模式；加 toggle 存在 localStorage。
- **评论回复（嵌套一层）**：mock-server 已有 `parentId` 字段和 replies 数组，UI 没接上；做出"回复"按钮即可激活嵌套评论。
- **RSS / Atom 全文输出**：README 提到 `rss.xml.js`，可以扩展为分类订阅、标签订阅。
- **阅读清单（read later）**：与 favorites 并列，但语义是"待读"；自动 7 天后归档。
- **"今年我写了 X 篇"年终回顾**：自动汇总当年文章 + 字数 + 评论数，做成 `/year/2026` 一次性页面。
- **置顶到期**：置顶加 `pinnedUntil` 字段，过期自动回落，让运营有"限时精选"能力。
- **AI 摘要**：对每篇文章自动生成 3 句话 TL;DR 放到 meta-panel，与 reading time 并列。

## 测试原始数据

- `GET /` → 200, 69940 B
- `GET /blog` → 200, 41253 B
- `GET /about` → 200, 26240 B
- `GET /blog/ai-developer-anxiety-new-work` → 200, 67369 B（含 TOC 5 项 / 7761 字 / 3 min）
- `GET /blog/this-does-not-exist` → 404（自定义 404 页）
- `POST /.netlify/functions/engagement action=like` → `{"liked":true,"likesCount":1}` ✓
- `POST action=comment author=体验者` → 立即 approved，UUID 正常返回 ✓
- `POST action=favorite` → 成功收藏，"favorites.title" 字段为空字符串（潜在 bug）
- `GET ?action=favorites` → 400 缺 slug（与 favorites 语义矛盾）❌

## 一句话总结

视觉与品牌立得住，主体功能可用，但 favorites 接口语义错、参数风格分裂、P2 UX 细节多——值得艾克本周内收一波。
