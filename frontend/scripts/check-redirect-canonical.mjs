#!/usr/bin/env node
/**
 * check-redirect-canonical —— 重定向页 canonical == 真实页 canonical（产物级断言）。
 *
 * 蔚 2026-11-07 工单#1：11-01 那次修错了对象（Base.astro 管不到重定向页——它们走
 * Astro 内置 redirects 模板）。本闸挂在 postbuild，扫 dist 里所有重定向页
 * （含 http-equiv=refresh 的 index.html），断言其 canonical 与目标真实页逐字相等，
 * 防再修错对象。退出码：0=全一致；1=有偏差（build 失败口径）。
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const DIST = new URL("../dist/", import.meta.url).pathname;
const BLOG = join(DIST, "blog");

if (!existsSync(BLOG)) {
  console.error("[redirect-canonical] dist/blog 不存在——先构建");
  process.exit(1);
}

const canonicalOf = (html) => {
  const hit = html.match(/rel="canonical" href="([^"]+)"/);
  return hit ? hit[1] : null;
};

const failures = [];
let checked = 0;
for (const slug of readdirSync(BLOG)) {
  const page = join(BLOG, slug, "index.html");
  if (!existsSync(page)) continue;
  const html = readFileSync(page, "utf8");
  if (!html.includes('http-equiv="refresh"')) continue; // 只管重定向页
  const refresh = html.match(/http-equiv="refresh" content="0;url=([^"]+)"/);
  const canonical = canonicalOf(html);
  if (!refresh || !canonical) {
    failures.push(`${slug}: 重定向页缺 refresh/canonical 结构`);
    continue;
  }
  const targetPath = refresh[1].replace(/\/$/, "");
  const targetSlug = targetPath.split("/").filter(Boolean).pop();
  const targetPage = join(BLOG, targetSlug, "index.html");
  if (!existsSync(targetPage)) {
    failures.push(`${slug}: 目标页 ${targetSlug} 不在产物中`);
    continue;
  }
  const targetCanonical = canonicalOf(readFileSync(targetPage, "utf8"));
  checked += 1;
  if (canonical !== targetCanonical) {
    failures.push(`${slug}:\n    重定向页 canonical = ${canonical}\n    真实页   canonical = ${targetCanonical}`);
  }
}

if (failures.length > 0) {
  console.error(`[redirect-canonical] ${failures.length} 处不一致（检查 ${checked} 页）：`);
  for (const f of failures) console.error(`  ✗ ${f}`);
  process.exit(1);
}
console.log(`[redirect-canonical] ${checked} 个重定向页 canonical 与真实页逐字一致`);
