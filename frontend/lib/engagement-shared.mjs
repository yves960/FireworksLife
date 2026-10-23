// 生产（netlify/functions/engagement.mjs）与本地 mock（scripts/mock-server.mjs）的共享层。
// 2026-10-23 工单教训：两侧各写一份必然分叉（mock 曾漏剔 HTML 标签、评论序列化停在旧版
// 泄漏 clientId 且无 isMine）。收敛到这里，一处修两处生效。
// 注：Netlify Functions 的 esbuild 打包支持相对路径 import。

export const sanitizeText = (value, maxLength = 120) =>
  String(value || '')
    .trim()
    .replace(/\s+/g, ' ')
    .replace(/<[^>]*>/g, '') // 双保险：入库前剔除 HTML 标签（评论不需要任何 HTML；前端另有 escapeHtml 转义）
    .slice(0, maxLength);

export const sanitizeSlug = (value) =>
  String(value || '').trim().replace(/[^a-zA-Z0-9-_]/g, '').slice(0, 120);

export const toPublicComment = (item, clientId = '') => ({
  id: item.id,
  author: item.author,
  content: item.content,
  createdAt: item.createdAt,
  parentId: item.parentId,
  status: item.status,
  // 身份比对只在服务端做，clientId 永不出站
  isMine: Boolean(clientId && item.clientId === clientId),
});

export const toPublicComments = (comments = [], clientId = '') =>
  comments
    .filter((item) => item.status === 'approved')
    .filter((item) => !item.parentId)
    .map((item) => ({
      ...toPublicComment(item, clientId),
      replies: comments
        .filter((reply) => reply.parentId === item.id && reply.status === 'approved')
        .map((reply) => toPublicComment(reply, clientId)),
    }));
