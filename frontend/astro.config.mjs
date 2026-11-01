import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// 上线域名（蔚 2026-11-01 P0/P1）：默认 fireworkslife.netlify.app（空置可占用），
// 环境变量 SITE_URL 可覆盖。旧值 yufu.netlify.app / yufu.blog 均被第三方占用，
// 严禁回填——tests/site-config.test.mjs 有防回归断言。
const SITE_URL = process.env.SITE_URL || 'https://fireworkslife.netlify.app';

export default defineConfig({
  site: SITE_URL,
  redirects: {
    '/blog/2026-04-04-how-to-build-and-optimize-a-skill': '/blog/how-to-build-and-optimize-a-skill',
    '/blog/2026-04-13-ai-developer-anxiety-new-work': '/blog/ai-developer-anxiety-new-work',
  },
  integrations: [mdx(), sitemap()],
  // 注意：Astro 顶层没有 server.proxy——代理必须配在 vite.server.proxy 下。
  // 旧写法（顶层 server.proxy）被静默忽略，dev 模式互动请求全打 404（2026-10-24 E2E 取证时发现）。
  vite: {
    server: {
      proxy: {
        '/.netlify/functions': {
          target: 'http://localhost:4322',
          changeOrigin: true,
        },
      },
    },
  },
});
