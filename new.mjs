import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const POSTS_DIR = 'src/content/posts';

const args = process.argv.slice(2);

// Parse -t flag
const typeIdx = args.indexOf('-t');
const postType = typeIdx >= 0 ? args[typeIdx + 1] : 'note';

// Title: everything except -t and its value
const titleArgs = args.filter((_, i) => {
  if (typeIdx >= 0 && (i === typeIdx || i === typeIdx + 1)) return false;
  return true;
});
const title = titleArgs.join(' ') || '';

const today = new Date().toISOString().slice(0, 10);
const desc = title
  ? title.toLowerCase().replace(/[^a-z0-9一-鿿]+/g, '-').replace(/^-|-$/g, '')
  : 'untitled';
const slug = `${today}-${desc}`;

const lines = ['---', `type: ${postType}`, `title: "${title || today}"`, `date: ${today}`];
if (postType === 'link') lines.push('link: ""');
lines.push('---', '');

if (!existsSync(POSTS_DIR)) mkdirSync(POSTS_DIR, { recursive: true });
const filepath = join(POSTS_DIR, `${slug}.md`);
writeFileSync(filepath, lines.join('\n'));
console.log(`Created: ${filepath}`);
