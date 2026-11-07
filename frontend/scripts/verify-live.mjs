#!/usr/bin/env node
/**
 * verify-live —— 上线验收七项 checklist 脚本化（蔚 11-07 工单#2，AGENTS.md 口径）。
 *
 * 用法：LIVE_BASE=https://fireworkslife.netlify.app node scripts/verify-live.mjs
 * （本地预演：cd frontend && npx astro preview & LIVE_BASE=http://localhost:4321 …）
 * 七项：探活本域 / 首页含「鱼腹」/ rss 200+items≥12+本域（单行文件须正则计数）/
 *      sitemap 200 本域 / canonical+og:url 本域带尾斜杠 / 真 404 / 评论 API 无 clientId。
 * 退出码：0=全过；1=有 FAIL（SKIP 不计败——本地无 Netlify 函数属预期）。
 */
const BASE = (process.env.LIVE_BASE || "https://fireworkslife.netlify.app").replace(/\/$/, "");
const DOMAIN = new URL(BASE).host;
// 期望域与探活域解耦：本地预演时 LIVE_BASE=localhost 而产物 canonical 是构建域——
// SITE_EXPECTED 覆盖比较基准（默认同 BASE，线上直跑无需设置）
const EXPECT = (process.env.SITE_EXPECTED ?? BASE).replace(/\/$/, "");

const results = [];
const record = (name, state, detail) => {
  results.push({ name, state, detail });
  console.log(`${state === "PASS" ? "✓" : state === "SKIP" ? "－" : "✗"} ${name}${detail ? ` —— ${detail}` : ""}`);
};

const fetchText = async (path) => {
  const resp = await fetch(`${BASE}${path}`, { redirect: "manual" });
  const text = await resp.text();
  return { resp, text };
};

try {
  // 1) 探活
  const home = await fetchText("/");
  if (home.resp.status !== 200) {
    record("探活", "FAIL", `HTTP ${home.resp.status}（未部署或被劫持；206B+404=空置）`);
  } else {
    record("探活", "PASS", `HTTP 200 (${DOMAIN})`);
  }

  // 2) 首页含「鱼腹」
  if (home.resp.status === 200) {
    record("首页品牌词", home.text.includes("鱼腹") ? "PASS" : "FAIL", "「鱼腹」在首页 HTML");
  }

  // 3) RSS：200 + items≥12 + 本域（单行文件——用正则计数，别信行数）
  const rss = await fetchText("/rss.xml");
  if (rss.resp.status !== 200) {
    record("rss.xml", "FAIL", `HTTP ${rss.resp.status}`);
  } else {
    const items = (rss.text.match(/<item>/g) || []).length;
    const linkOk = rss.text.includes(`<link>${EXPECT}/</link>`) || rss.text.includes(EXPECT);
    record("rss.xml", items >= 12 && linkOk ? "PASS" : "FAIL", `items=${items}（≥12）${linkOk ? "" : "，channel.link 非本域"}`);
  }

  // 4) sitemap 本域
  const sitemap = await fetchText("/sitemap-index.xml");
  const expectHost = new URL(EXPECT).host;
  record("sitemap", sitemap.resp.status === 200 && sitemap.text.includes(expectHost) ? "PASS" : "FAIL", `HTTP ${sitemap.resp.status}${sitemap.text.includes(expectHost) ? "" : "，非本域"}`);

  // 5) canonical + og:url 本域带尾斜杠
  if (home.resp.status === 200) {
    const canonical = home.text.match(/rel="canonical" href="([^"]+)"/)?.[1] ?? null;
    const ogUrl = home.text.match(/property="og:url" content="([^"]+)"/)?.[1] ?? null;
    const ok = (u) => u !== null && u === `${EXPECT}/`;
    record("canonical/og:url", ok(canonical) && ok(ogUrl) ? "PASS" : "FAIL", `canonical=${canonical} og:url=${ogUrl}（期望 ${EXPECT}/）`);
  }

  // 6) 随机不存在路径 → 真 404（防 SPA 兜底复活）
  const ghost = await fetch(`${BASE}/zzz-not-a-page-${Date.now()}`);
  record("真 404", ghost.status === 404 ? "PASS" : "FAIL", `HTTP ${ghost.status}（期望 404，200=有兜底）`);

  // 7) 评论 API 无 clientId（Netlify 函数；本地预览无函数 → SKIP）
  const api = await fetch(`${BASE}/api/engagement?path=/`);
  if (api.status === 404) {
    record("评论 API 无 clientId", "SKIP", "函数未部署（本地预演属预期；线上 404=函数缺失，部署后复查）");
  } else {
    const body = await api.text();
    record("评论 API 无 clientId", body.includes("clientId") ? "FAIL" : "PASS", `HTTP ${api.status}${body.includes("clientId") ? "，泄漏 clientId" : ""}`);
  }
} catch (error) {
  record("网络可达性", "FAIL", String(error.cause?.code ?? error.message));
}

const fails = results.filter((r) => r.state === "FAIL").length;
const skips = results.filter((r) => r.state === "SKIP").length;
console.log(`\nverify-live：${results.length - fails - skips} PASS / ${fails} FAIL / ${skips} SKIP（base=${BASE}）`);
process.exit(fails > 0 ? 1 : 0);
