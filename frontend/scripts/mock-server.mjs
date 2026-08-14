#!/usr/bin/env node
/**
 * Mock server for local development of Netlify Functions (engagement endpoint).
 *
 * Usage:
 *   node scripts/mock-server.mjs          # starts on port 4322
 *   MOCK_PORT=3001 node scripts/mock-server.mjs
 *
 * Add to package.json scripts:
 *   "mock": "node scripts/mock-server.mjs"
 *
 * Then in astro.config.mjs, proxy /.netlify/functions/* to this server,
 * or just configure the dev server proxy.
 */

import { createServer } from 'node:http';

const PORT = Number(process.env.MOCK_PORT) || 4322;

// In-memory store
const store = {
  posts: {},
  favorites: {},
};

function json(res, status, body) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, x-client-id',
  });
  res.end(JSON.stringify(body));
}

function getPostState(slug) {
  if (!store.posts[slug]) {
    store.posts[slug] = { comments: [], likesBy: {}, rateLimit: {} };
  }
  return store.posts[slug];
}

function getFavorites(clientId) {
  return store.favorites[clientId] || [];
}

function toPublicComments(comments = []) {
  return comments
    .filter((c) => c.status === 'approved')
    .filter((c) => !c.parentId)
    .map((c) => ({
      ...c,
      replies: comments.filter((r) => r.parentId === c.id && r.status === 'approved'),
    }));
}

function sanitizeText(value, maxLength = 120) {
  return String(value || '').trim().replace(/\s+/g, ' ').slice(0, maxLength);
}

function sanitizeSlug(value) {
  return String(value || '').trim().replace(/[^a-zA-Z0-9-_]/g, '').slice(0, 120);
}

const server = createServer((req, res) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    json(res, 204, null);
    return;
  }

  const url = new URL(req.url, `http://localhost:${PORT}`);
  const clientId = req.headers['x-client-id'] || url.searchParams.get('clientId') || '';

  // Route: engagement
  if (url.pathname === '/.netlify/functions/engagement') {
    if (req.method === 'GET') {
      const view = url.searchParams.get('view');
      if (view === 'favorites') {
        return json(res, 200, { favorites: getFavorites(clientId) });
      }

      const slug = sanitizeSlug(url.searchParams.get('slug'));
      if (!slug) return json(res, 400, { error: '缺少 slug' });

      const postState = getPostState(slug);
      const favorites = getFavorites(clientId);

      return json(res, 200, {
        moderationMode: 'auto',
        liked: Boolean(clientId && postState.likesBy?.[clientId]),
        likesCount: Object.keys(postState.likesBy || {}).length,
        favorited: favorites.some((f) => f.slug === slug),
        comments: toPublicComments(postState.comments || []),
      });
    }

    if (req.method === 'POST') {
      let body = '';
      req.on('data', (chunk) => { body += chunk; });
      req.on('end', () => {
        let data;
        try { data = JSON.parse(body); } catch { data = {}; }

        const action = sanitizeText(data.action, 24);
        const slug = sanitizeSlug(data.slug);
        if (!slug) return json(res, 400, { error: '缺少 slug' });

        const postState = getPostState(slug);

        if (action === 'like') {
          if (!clientId) return json(res, 400, { error: '缺少客户端标识' });
          postState.likesBy ||= {};
          if (postState.likesBy[clientId]) {
            delete postState.likesBy[clientId];
          } else {
            postState.likesBy[clientId] = true;
          }
          return json(res, 200, {
            liked: Boolean(postState.likesBy[clientId]),
            likesCount: Object.keys(postState.likesBy).length,
          });
        }

        if (action === 'favorite') {
          if (!clientId) return json(res, 400, { error: '缺少客户端标识' });
          const title = sanitizeText(data.title, 160);
          const favorites = getFavorites(clientId);
          const exists = favorites.some((f) => f.slug === slug);
          const nextFavorites = exists
            ? favorites.filter((f) => f.slug !== slug)
            : [...favorites, { slug, title, savedAt: new Date().toISOString() }];
          store.favorites[clientId] = nextFavorites;
          return json(res, 200, { favorited: !exists, favorites: nextFavorites });
        }

        if (action === 'comment') {
          if (!clientId) return json(res, 400, { error: '缺少客户端标识' });
          const author = sanitizeText(data.author || '匿名', 24);
          const content = sanitizeText(data.content, 300);
          const parentId = sanitizeText(data.parentId, 80);
          if (!content) return json(res, 400, { error: '评论不能为空' });

          if (parentId && !(postState.comments || []).some((c) => c.id === parentId)) {
            return json(res, 400, { error: '回复目标不存在' });
          }

          const now = Date.now();
          const lastAt = postState.rateLimit?.[clientId] || 0;
          if (now - lastAt < 15_000) {
            return json(res, 429, { error: '发得有点快，15 秒后再试。' });
          }

          postState.comments ||= [];
          postState.rateLimit ||= {};
          postState.comments.push({
            id: crypto.randomUUID(),
            clientId,
            author,
            content,
            parentId: parentId || '',
            status: 'approved',
            createdAt: new Date().toISOString(),
          });
          postState.rateLimit[clientId] = now;

          return json(res, 200, {
            moderationMode: 'auto',
            pending: false,
            comments: toPublicComments(postState.comments),
          });
        }

        if (action === 'delete-comment') {
          if (!clientId) return json(res, 400, { error: '缺少客户端标识' });
          const commentId = sanitizeText(data.commentId, 80);
          const target = (postState.comments || []).find((c) => c.id === commentId);
          if (!target) return json(res, 404, { error: '评论不存在' });
          if (target.clientId !== clientId) return json(res, 403, { error: '只能删除自己的评论' });

          postState.comments = (postState.comments || []).filter(
            (c) => c.id !== commentId && c.parentId !== commentId,
          );
          return json(res, 200, { comments: toPublicComments(postState.comments) });
        }

        return json(res, 400, { error: '不支持的 action' });
      });
      return;
    }

    return json(res, 405, { error: 'Method Not Allowed' });
  }

  // 404 for everything else
  json(res, 404, { error: 'Not Found' });
});

server.listen(PORT, () => {
  console.log(`🐟 Mock engagement server → http://localhost:${PORT}`);
  console.log(`   Endpoint: /.netlify/functions/engagement`);
});
