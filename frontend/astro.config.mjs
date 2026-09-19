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
  server: {
    proxy: {
      '/.netlify/functions': {
        target: 'http://localhost:4322',
        changeOrigin: true,
      },
    },
  },
});
