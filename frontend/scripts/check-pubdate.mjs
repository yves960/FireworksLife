// 护栏：frontmatter 里 pubDate 留空会让 z.coerce.date() 静默吃成 epoch(1970-1-1)。
// 本脚本在 build 前置阶段强制拦截（package.json: build = check:content && astro build）。
import { readdirSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'src', 'content', 'blog');
const bad = readdirSync(dir)
  .filter((name) => name.endsWith('.md') || name.endsWith('.mdx'))
  .filter((name) => /^pubDate:\s*$/m.test(readFileSync(path.join(dir, name), 'utf8')));

if (bad.length) {
  console.error('[check-pubdate] 以下文章的 pubDate 为空，请在 frontmatter 填入真实发布日期：');
  for (const name of bad) console.error(`  - ${name}`);
  process.exit(1);
}
console.log('[check-pubdate] OK：所有文章 pubDate 均已填写');
