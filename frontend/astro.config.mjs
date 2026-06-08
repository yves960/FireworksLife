import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yufu.netlify.app',
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
