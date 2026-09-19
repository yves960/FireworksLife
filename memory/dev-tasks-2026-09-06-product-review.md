# [工单] 2026-09-06 产品体验发现的 P0/P1 - 需艾克接手

> 来源：蔚（Director）产品体验 · 完整笔记：workspace-director/memory/products/FireworksLife-2026-09-06.md
> 注：跨 agent 直发被网关策略拦截（tools.agentToAgent 未启用），落此工单交接。

## P0 - 线上部署错乱（当天修）
- `https://yufu.netlify.app/` 首页是 "Gesture Particle System"（非本博客），`/blog` 404
- `frontend/astro.config.mjs` 的 `site` 指向错误/被占用的域名 → sitemap 全错
- 动作：确认真实域名 → 改 site → 重部署

## P1 - 安全：评论 API 泄漏 clientId
- `frontend/netlify/functions/engagement.mjs` 的 `toPublicComments` 用 `{...item}` 展开，公开返回 clientId（唯一身份凭证）
- 任何人可拿他人 clientId 冒充发评论/删评论
- 修法：服务端剔除 clientId；前端"我的评论"判断（`item.clientId === clientId`）改为服务端比对后返回 `isMine`

## P1 - 重复文章双上线
- `content/blog/how-to-build-and-optimize-skill.md`（title "flow-trace"）与 `2026-04-04-how-to-build-and-optimize-a-skill.md` 内容几乎相同
- 动作：删旧版留带日期版

## P2
1. Base.astro 补 og:/twitter card/canonical
2. 拆巨石文件：index.astro(1162行)/[slug].astro(1098行) → 组件化

## 新功能想法
RSS 订阅 / 按标签推荐相关文章 / 评论表情回应
