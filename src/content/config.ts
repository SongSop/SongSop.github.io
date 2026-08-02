import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  schema: z.object({
    type: z.enum(['article', 'note', 'link']).default('article'),
    title: z.string().optional(),
    date: z.date(),
    link: z.string().optional(),
  }),
});

export const collections = { posts };
