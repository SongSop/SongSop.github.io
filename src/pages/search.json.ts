import { getCollection } from 'astro:content';

export async function GET() {
  const posts = await getCollection('posts');
  const searchData = posts.map(p => {
    // Extract plain text from body (strip markdown syntax roughly)
    const text = p.body
      .replace(/^---[\s\S]*?---/m, '') // frontmatter
      .replace(/```[\s\S]*?```/g, ' ') // fenced code blocks
      .replace(/`[^`]+`/g, ' ') // inline code
      .replace(/[#*[\]()>|$!\-_=:<>]/g, ' ') // markdown syntax
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 5000);

    return {
      title: p.data.title || '',
      date: p.data.date.toISOString().slice(0, 10),
      slug: p.slug,
      type: p.data.type || 'article',
      text,
    };
  });

  return new Response(JSON.stringify(searchData, null, 2), {
    headers: { 'Content-Type': 'application/json' },
  });
}
