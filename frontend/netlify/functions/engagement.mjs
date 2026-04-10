import { getStore } from '@netlify/blobs';

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
    },
  });

const sanitizeText = (value, maxLength = 120) =>
  String(value || '')
    .trim()
    .replace(/\s+/g, ' ')
    .slice(0, maxLength);

const sanitizeSlug = (value) =>
  String(value || '')
    .trim()
    .replace(/[^a-zA-Z0-9-_]/g, '')
    .slice(0, 120);

const getClientId = (request, url) =>
  request.headers.get('x-client-id') || url.searchParams.get('clientId') || '';

async function getPostState(slug) {
  const store = getStore('yufu-engagement');
  return (
    (await store.get(`posts/${slug}`, { type: 'json' })) || {
      comments: [],
      likesBy: {},
    }
  );
}

async function getFavorites(clientId) {
  if (!clientId) return [];
  const store = getStore('yufu-engagement');
  return (await store.get(`favorites/${clientId}`, { type: 'json' })) || [];
}

async function savePostState(slug, state) {
  const store = getStore('yufu-engagement');
  await store.setJSON(`posts/${slug}`, state);
}

async function saveFavorites(clientId, favorites) {
  const store = getStore('yufu-engagement');
  await store.setJSON(`favorites/${clientId}`, favorites);
}

export default async (request) => {
  const url = new URL(request.url);
  const clientId = getClientId(request, url);

  if (request.method === 'GET') {
    const view = url.searchParams.get('view');

    if (view === 'favorites') {
      return json(200, { favorites: await getFavorites(clientId) });
    }

    const slug = sanitizeSlug(url.searchParams.get('slug'));
    if (!slug) {
      return json(400, { error: '缺少 slug' });
    }

    const postState = await getPostState(slug);
    const favorites = await getFavorites(clientId);

    return json(200, {
      liked: Boolean(clientId && postState.likesBy?.[clientId]),
      likesCount: Object.keys(postState.likesBy || {}).length,
      favorited: favorites.some((item) => item.slug === slug),
      comments: postState.comments || [],
    });
  }

  if (request.method !== 'POST') {
    return json(405, { error: 'Method Not Allowed' });
  }

  const body = await request.json().catch(() => ({}));
  const action = sanitizeText(body.action, 24);
  const slug = sanitizeSlug(body.slug);

  if (!slug) {
    return json(400, { error: '缺少 slug' });
  }

  const postState = await getPostState(slug);

  if (action === 'like') {
    if (!clientId) {
      return json(400, { error: '缺少客户端标识' });
    }

    postState.likesBy ||= {};
    if (postState.likesBy[clientId]) {
      delete postState.likesBy[clientId];
    } else {
      postState.likesBy[clientId] = true;
    }

    await savePostState(slug, postState);

    return json(200, {
      liked: Boolean(postState.likesBy[clientId]),
      likesCount: Object.keys(postState.likesBy).length,
    });
  }

  if (action === 'favorite') {
    if (!clientId) {
      return json(400, { error: '缺少客户端标识' });
    }

    const title = sanitizeText(body.title, 160);
    const favorites = await getFavorites(clientId);
    const exists = favorites.some((item) => item.slug === slug);
    const nextFavorites = exists
      ? favorites.filter((item) => item.slug !== slug)
      : [...favorites, { slug, title, savedAt: new Date().toISOString() }];

    await saveFavorites(clientId, nextFavorites);
    return json(200, {
      favorited: !exists,
      favorites: nextFavorites,
    });
  }

  if (action === 'comment') {
    const author = sanitizeText(body.author || '匿名', 24);
    const content = sanitizeText(body.content, 300);

    if (!content) {
      return json(400, { error: '评论不能为空' });
    }

    postState.comments ||= [];
    postState.comments.push({
      id: crypto.randomUUID(),
      author,
      content,
      createdAt: new Date().toISOString(),
    });

    await savePostState(slug, postState);
    return json(200, { comments: postState.comments });
  }

  return json(400, { error: '不支持的 action' });
};
