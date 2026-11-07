// site-config —— 蔚 2026-11-01 P1 防回归：site 不得指向已知被第三方占用的域名。
// 旧值 'https://yufu.netlify.app' 让全站 canonical/og:url/RSS/sitemap 给别人导流。
// 默认值方案：fireworkslife.netlify.app（空置可占用）；SITE_URL 环境变量可覆盖。
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const config = readFileSync(new URL('../astro.config.mjs', import.meta.url), 'utf8');

const OCCUPIED_DOMAINS = ['yufu.netlify.app', 'yufu.blog'];

test('site 配置不指向已知被占域名（防第三方导流回归）', () => {
  for (const domain of OCCUPIED_DOMAINS) {
    assert.ok(
      !config.includes(`https://${domain}`),
      `astro.config 的 site 不得指向被第三方占用的域名 ${domain}（canonical/RSS/sitemap 全链导流）`,
    );
  }
});

test('redirects 目标必须带尾斜杠（重定向页 canonical 与真实页一致的前提）', () => {
  const redirectBlock = config.match(/redirects:\s*\{[\s\S]*?\n\s*\}/);
  assert.ok(redirectBlock, 'astro.config 应有 redirects 块');
  const targets = [...redirectBlock[0].matchAll(/'\s*:\s*'([^']+)'/g)].map((m) => m[1]);
  assert.ok(targets.length >= 2, `应有至少 2 条重定向（含 2026-04-04/13 两条），实得 ${targets.length}`);
  for (const target of targets) {
    assert.ok(target.endsWith('/'), `重定向目标必须带尾斜杠: ${target}`);
  }
});

test('site 走 SITE_URL 注入或默认 fireworkslife.netlify.app（P0 默认值方案）', () => {
  assert.ok(
    config.includes('process.env.SITE_URL') && config.includes('fireworkslife.netlify.app'),
    'site 应为 process.env.SITE_URL 注入、默认 fireworkslife.netlify.app',
  );
});
