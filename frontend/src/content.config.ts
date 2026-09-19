import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce
      .date()
      .refine((date) => date.getTime() > 946684800_000, {
        message: 'pubDate 不能为空或无效（拒绝 1970 epoch，请在 frontmatter 填入真实发布日期）',
      }),
    category: z.string().default('默认'),
    subTag: z.string().optional(),
    tags: z.array(z.string()).optional(),
    cover: z.string().optional(),
  }),
});

export const collections = { blog };
