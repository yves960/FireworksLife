import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yufu.netlify.app',
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
