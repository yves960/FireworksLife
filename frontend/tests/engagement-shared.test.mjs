// 契约测试（node --test，零依赖）：蔚 10-24 工单 P1-2
// 覆盖：XSS payload、engagement 响应字段完备（计数不闪空）、reset-mock 幂等、
// mock 与共享序列化逐字段相等（防 10-23 之前的 mock/生产分叉复发）。
// 单命令入口：npm run verify（= check:content + test + build）
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

import { sanitizeText, sanitizeSlug, toPublicComments } from '../lib/engagement-shared.mjs';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PORT = 4390 + Math.floor(Math.random() * 50);
const BASE = `http://127.0.0.1:${PORT}`;

async function startMock() {
  const child = spawn(process.execPath, [path.join(ROOT, 'scripts', 'mock-server.mjs')], {
    env: { ...process.env, MOCK_PORT: String(PORT) },
    stdio: 'ignore',
  });
  for (let i = 0; i < 40; i += 1) {
    try {
      await fetch(`${BASE}/.netlify/functions/engagement?slug=probe&clientId=p`, {
        headers: { 'x-client-id': 'probe' },
      });
      return child;
    } catch {
      await new Promise((r) => setTimeout(r, 100));
    }
  }
  throw new Error('mock server 启动超时');
}

const api = (pathname, init) => fetch(`${BASE}${pathname}`, init);

test('XSS payload：标签全剔、正文保留（共享 sanitizeText）', () => {
  assert.equal(sanitizeText('<img src=x onerror=alert(1)>hello'), 'hello');
  assert.equal(sanitizeText('<b>bold</b>text'), 'boldtext');
  assert.equal(sanitizeText('  多   空格\n文本  '), '多 空格 文本');
});

test('sanitizeSlug 只留 [a-zA-Z0-9-_]', () => {
  assert.equal(sanitizeSlug('../evil path!'), 'evilpath');
});

test('toPublicComments：clientId 永不出站 + isMine 主楼/回复独立判定', () => {
  const comments = [
    { id: 'a', clientId: 'X', author: '甲', content: 'hi', createdAt: 't1', parentId: '', status: 'approved' },
    { id: 'b', clientId: 'Y', author: '乙', content: 're', createdAt: 't2', parentId: 'a', status: 'approved' },
  ];
  const out = toPublicComments(comments, 'X');
  assert.equal(JSON.stringify(out).includes('clientId'), false);
  assert.equal(out[0].isMine, true);
  assert.equal(out[0].replies[0].isMine, false);
});

test('mock E2E：评论带 XSS payload 落库即净化，响应与共享序列化逐字段相等', async () => {
  const mock = await startMock();
  try {
    const posted = await api('/.netlify/functions/engagement', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-client-id': 'e2e-user' },
      body: JSON.stringify({
        slug: 'contract-test',
        action: 'comment',
        author: '<b>攻击者</b>',
        content: '<img src=x onerror=alert(1)>正经评论',
      }),
    });
    assert.equal(posted.status, 200);
    const data = await posted.json();

    // 共享函数直算的期望值（模拟同一条"已净化入库"的数据）
    const expected = toPublicComments(
      [
        {
          id: data.comments[0].id,
          clientId: 'e2e-user',
          author: '攻击者',
          content: '正经评论',
          createdAt: data.comments[0].createdAt,
          parentId: '',
          status: 'approved',
        },
      ],
      'e2e-user'
    );
    assert.deepEqual(data.comments, expected);
    assert.equal(data.comments[0].isMine, true);
  } finally {
    mock.kill();
  }
});

test('mock E2E：GET 字段完备（liked/likesCount/favorited/comments 永远有值，计数不闪空）', async () => {
  const mock = await startMock();
  try {
    const res = await api('/.netlify/functions/engagement?slug=shape-test', {
      headers: { 'x-client-id': 'shape-user' },
    });
    const data = await res.json();
    assert.equal(typeof data.likesCount, 'number');
    assert.ok(data.likesCount >= 0);
    assert.equal(typeof data.liked, 'boolean');
    assert.equal(typeof data.favorited, 'boolean');
    assert.ok(Array.isArray(data.comments));
    assert.equal(typeof data.moderationMode, 'string');
  } finally {
    mock.kill();
  }
});

test('reset-mock 幂等：连续两次 reset 结果一致且数据归零', async () => {
  const mock = await startMock();
  try {
    await api('/.netlify/functions/engagement', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-client-id': 'reset-user' },
      body: JSON.stringify({ slug: 'reset-test', action: 'comment', author: '甲', content: '会被清掉的' }),
    });

    const first = await api('/__reset', { method: 'POST' }).then((r) => r.json());
    const second = await api('/__reset', { method: 'POST' }).then((r) => r.json());
    assert.deepEqual(first, second);
    assert.equal(first.reset, true);

    const after = await api('/.netlify/functions/engagement?slug=reset-test', {
      headers: { 'x-client-id': 'reset-user' },
    }).then((r) => r.json());
    assert.deepEqual(after.comments, []);
  } finally {
    mock.kill();
  }
});
